import asyncio

from pykrotik import Client


async def main():
    client = Client(host="localhost", username="admin", password="")
    await client.list_ip_dns_records()


if __name__ == "__main__":
    asyncio.run(main())
