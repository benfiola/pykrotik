import os
import pathlib

import packaging
import toml
from common import log, run_cmd


def get_next_version(*, as_tag: bool = False) -> str:
    command = ["semantic-release", "--noop", "--strict", "version"]
    if as_tag is True:
        command.extend(["--print-tag"])
    else:
        command.extend(["--print"])
    env = {"GH_TOKEN": "undefined", **os.environ}
    return run_cmd(command, env=env).strip()


def main():
    log("publishing package")

    log("determining version of package")
    version = get_next_version()
    log(f"version: {version}")

    log("writing project version")
    pyproject_file = pathlib.Path.cwd().joinpath("pyproject.toml")
    if not pyproject_file.exists():
        raise FileNotFoundError(pyproject_file)
    data = toml.loads(pyproject_file.read_text())
    data["project"]["version"] = version
    name = data["project"]["name"]
    pyproject_file.write_text(toml.dumps(data))

    log("building package")
    run_cmd(["python", "-m", "build"])


if __name__ == "__main__":
    main()
