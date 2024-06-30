#!/usr/bin/env python3
import os
import pathlib
import shutil

import packaging.utils
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
    version_file = pathlib.Path.cwd().joinpath(".github-version")
    version_file.write_text(version)

    log("determining tag of package")
    tag = get_next_version(as_tag=True)
    log(f"tag: {tag}")
    tag_file = pathlib.Path.cwd().joinpath(".github-tag")
    tag_file.write_text(tag)

    log("writing project version")
    pyproject_file = pathlib.Path.cwd().joinpath("pyproject.toml")
    if not pyproject_file.exists():
        raise FileNotFoundError(pyproject_file)
    data = toml.loads(pyproject_file.read_text())
    data["project"]["version"] = version
    name = data["project"]["name"]
    pyproject_file.write_text(toml.dumps(data))

    dist_folder = pathlib.Path.cwd().joinpath("dist")
    if dist_folder.exists():
        log(f"deleting existing dist folder")
        shutil.rmtree(dist_folder)
    log("building package")
    run_cmd(["python", "-m", "build"])
    pkg_name = packaging.utils.canonicalize_name(name)
    pkg_version = packaging.utils.canonicalize_version(version)
    log(f"package name: {pkg_name}")
    log(f"package version: {pkg_version}")
    files = [
        dist_folder.joinpath(f"{pkg_name}-{pkg_version}.tar.gz"),
        dist_folder.joinpath(f"{pkg_name}-{pkg_version}-py3-none-any.whl"),
    ]
    for file in files:
        if not file.exists():
            raise FileNotFoundError(file)

    log("publishing package")
    # run_cmd(["python", "-m", "twine", "upload", *[str(f) for f in files]])


if __name__ == "__main__":
    main()
