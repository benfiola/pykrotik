import io
import os
import shlex
import subprocess
import sys
import threading


def log(message: str):
    print(f"> {message}", file=sys.stderr)


def run_cmd(cmd: list[str], **kwargs):
    buffer_stdout = io.StringIO()
    buffer_stderr = io.StringIO()

    def _reader(role: str):
        nonlocal buffer_stdout, buffer_stderr, popen
        if role == "stdout":
            in_buffer = popen.stdout
            out_buffer = buffer_stdout
        elif role == "stderr":
            in_buffer = popen.stderr
            out_buffer = buffer_stderr
        else:
            raise NotImplementedError()

        def read():
            if in_buffer is None:
                raise RuntimeError()
            data = in_buffer.read()
            if data is None:
                return
            out_buffer.write(data)
            sys.stderr.write(data)

        while popen.returncode is not None:
            read()
        read()

    cmd_str = f"{shlex.join(cmd)}"
    if env := kwargs.get("env"):
        diff = {}
        for key, value in env.items():
            if os.environ.get(key) == value:
                continue
            diff[key] = value
        diff_str = " ".join(f"{k}={v}" for k, v in diff.items())
        if diff_str:
            cmd_str += f" (env: {diff_str})"
    if cwd := kwargs.get("cwd"):
        cmd_str += f" (cwd: {cwd})"

    print(f"$ {cmd_str}", file=sys.stderr)
    kwargs["encoding"] = "utf-8"
    kwargs["stdout"] = subprocess.PIPE
    kwargs["stderr"] = subprocess.PIPE
    popen = subprocess.Popen(cmd, **kwargs)
    readers = [
        threading.Thread(target=lambda: _reader("stdout")),
        threading.Thread(target=lambda: _reader("stderr")),
    ]
    [r.start() for r in readers]
    popen.wait()
    [r.join() for r in readers]

    buffer_stdout.seek(0)
    buffer_stderr.seek(0)
    stdout = buffer_stdout.read()
    stderr = buffer_stderr.read()
    if popen.returncode != 0:
        raise subprocess.CalledProcessError(
            cmd=cmd, output=stdout, returncode=popen.returncode, stderr=stderr
        )
    return stdout
