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
