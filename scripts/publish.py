import io
import shlex
import subprocess
import sys
import threading


def log(message: str):
    print(f"> {message}", file=sys.stderr)


def run_cmd(cmd: list[str]):
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

    log(f"{shlex.join(cmd)}")
    popen = subprocess.Popen(
        cmd, encoding="utf-8", stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    readers = [
        threading.Thread(target=lambda: _reader("stdout")),
        threading.Thread(target=lambda: _reader("stderr")),
    ]
    [r.start() for r in readers]
    popen.wait()
    [r.join() for r in readers]

    stdout = buffer_stdout.read()
    stderr = buffer_stderr.read()
    if popen.returncode != 0:
        raise subprocess.CalledProcessError(
            cmd=cmd, output=stdout, returncode=popen.returncode, stderr=stderr
        )
    return stdout


def get_next_version(*, as_tag: bool = False) -> str:
    command = ["semantic-release", "--noop", "--strict", "version"]
    if as_tag is True:
        command.extend(["--print-tag"])
    else:
        command.extend(["--print"])
    return run_cmd(command).strip()


def main():
    version = get_next_version()
    print(version)


if __name__ == "__main__":
    main()
