# pykrotik

Pykrotik is an async client capable of interacting with the [Mikrotik RouterOS api](https://help.mikrotik.com/docs/display/ROS/API). It has a pretty straightforward collection of functions and objects that match
what's provided in RouterOS.

NOTE: While this client will forever be incomplete (RouterOS has a lot of APIs) - this client has a
robust foundation and can be forked and extended as needed.

---

## Installation

```shell
pip install pykrotik
```

## Example Usage

```python
from pykrotik import Client, IpDnsARecord

client = Client(
    hostname="<host>",
    username="username",
    password="password"
)
records = await client.list_ip_dns_records()
await client.set_ip_dns_record_comment(records[0], "comment")
await client.delete_ip_dns_record[records[-1]]
```

## Development

I personally use [vscode](https://code.visualstudio.com/) as an IDE. For a consistent development experience, this project is also configured to utilize [devcontainers](https://containers.dev/). If you're using both - and you have the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) installed - you can follow the [introductory docs](https://code.visualstudio.com/docs/devcontainers/tutorial) to quickly get started.

NOTE: Helper scripts are written under the assumption that they're being executed within a dev container.

### Creating a routeros docker container

From the project root, run the following to create a routeros docker container to test the client with:

```shell
cd /workspaces/pykrotik
./dev/create-router.sh
```

This will:

- Delete an routeros docker container if it exists
- Create a new routeros docker container

### Creating a launch script

Copy the [dev.template.py](./dev.template.py) script to `dev.py`, then run it to start the client.

If placed in the top-level directory, `dev.py` is gitignored and you can change this file as needed without worrying about committing it to git.

Additionally, the devcontainer is configured with vscode launch configurations that point to a top-level `dev.py` file. You should be able to launch (and attach a debugger to) the client by launching it natively through vscode.
