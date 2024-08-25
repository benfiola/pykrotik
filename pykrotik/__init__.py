import asyncio
import datetime
import enum
import logging
import uuid
from typing import Annotated, Any, Literal, Union

import pydantic

logger = logging.getLogger(__name__)


class BaseModel(pydantic.BaseModel):
    """
    Defines a base model from which other models can be defined
    """

    # config that:
    #  - allows models to be populated by alias and field name
    model_config = pydantic.ConfigDict(populate_by_name=True)


class IpAddress(BaseModel):
    # the ip address
    address: str
    # comment attached to the ip address
    comment: str = pydantic.Field(default="")
    # the network the address belongs to
    network: str
    # the interface the address is attached to
    interface: str


class IpFirewallAddressList(BaseModel):
    # NOTE: Address list is a misnomer - these are individual addresses.  Those with a common 'list' field belong to the same list.

    # the ip address
    address: str
    # comment attached to the ip firewall address list
    comment: str = pydantic.Field(default="")
    # the date the address was created
    creation_time: datetime.datetime | None = pydantic.Field(
        default=None, alias=str("creation-time")
    )
    # flag that dictates whether an ip firewall address list is active
    disabled: bool = pydantic.Field(default=False)
    # the id for an ip firewall address list (NOTE: prefixed with '*')
    id: str | None = pydantic.Field(default=None, alias=str(".id"))
    # the list the ip address belongs to
    list: str
    # the timeout for the address list record
    timeout: int | None = pydantic.Field(default=None)


class IpFirewallProtocol(str, enum.Enum):
    """
    List of protocols selectable when defining ip firewall nat rules
    """

    Dccp = "dccp"
    Ddp = "ddp"
    Egp = "egp"
    Encap = "encap"
    Etherip = "etherip"
    Ggp = "ggp"
    Gre = "gre"
    Hmp = "hmp"
    Icmp = "icmp"
    IdprCmtp = "idpr-cmtp"
    Igmp = "igmp"
    IpEncap = "ip-encap"
    Ipip = "ipip"
    IpsecAh = "ipsec-ah"
    IpsecEsp = "ipsec-esp"
    Ipv6Encap = "ipv6-encap"
    IsoTp4 = "iso-tp4"
    L2tp = "l2tp"
    Ospf = "ospf"
    Pim = "pim"
    Pup = "pup"
    Rdp = "rdp"
    Rspf = "rspf"
    Rsvp = "rsvp"
    Sctp = "sctp"
    St = "st"
    Tcp = "tcp"
    Udp = "udp"
    UdpLite = "udp-lite"
    Vmtp = "vmtp"
    Vrrp = "vrrp"
    XnsIdp = "xns-idp"
    Xtp = "xtp"


class IpFirewallNatAction(str, enum.Enum):
    """
    Ip firewall nat actions supported by routeros
    """

    Accept = "accept"
    AddDstToAddressList = "add-dst-to-address-list"
    AddSrcToAddressList = "add-src-to-address-list"
    DstNat = "dst-nat"
    EndpointIndependentNat = "endpoint-independent-nat"
    Jump = "jump"
    Log = "log"
    Masquerade = "masquerade"
    Netmap = "netmap"
    Passthrough = "passthrough"
    Redirect = "redirect"
    Return = "return"
    Same = "same"
    SrcNat = "src-nat"


class IpFirewallNat(BaseModel):
    """
    Definition of an ip firewall nat
    """

    # the action the firewall filter will take
    action: IpFirewallNatAction
    # action-specific address list field
    address_list: str | None = pydantic.Field(default=None, alias=str("address-list"))
    # protocol-specific field representing a source/destination port
    any_port: str | None = pydantic.Field(default=None, alias=str("any-port"))
    # the chain the firewall filter belongs to
    chain: str
    # comment attached to the ip firewall filter
    comment: str = pydantic.Field(default="")
    # flag that dictates whether an ip firewall filter is active
    disabled: bool = pydantic.Field(default=False)
    # dst address for the firewall fitler
    dst_address: str | None = pydantic.Field(default=None, alias=str("dst-address"))
    # dst address list for the firewall fitler
    dst_address_list: str | None = pydantic.Field(
        default=None, alias=str("dst-address-list")
    )
    # protocol-specific field representing a destination port
    dst_port: str | None = pydantic.Field(default=None, alias=str("dst-port"))
    # the id for an ip firewall filter (NOTE: prefixed with '*')
    id: str | None = pydantic.Field(default=None, alias=str(".id"))
    # action-specific jump target
    jump_target: str | None = pydantic.Field(default=None, alias=str("jump-target"))
    # flag that dictates whether filter is logged
    log: bool = pydantic.Field(default=False)
    # log prefix for logged filter
    log_prefix: str = pydantic.Field(default="", alias=str("log-prefix"))
    # protocol for the nat filter
    protocol: IpFirewallProtocol | None = pydantic.Field(default=None)
    # src address for the firewall fitler
    src_address: str | None = pydantic.Field(default=None, alias=str("src-address"))
    # src address list for the firewall fitler
    src_address_list: str | None = pydantic.Field(
        default=None, alias=str("src-address-list")
    )
    # protocol-specific field representing a source port
    src_port: str | None = pydantic.Field(default=None, alias=str("src-port"))
    # action-specific field representing a target address
    to_addresses: str | None = pydantic.Field(default=None, alias=str("to-addresses"))
    # action-specific field representing a target port
    to_ports: str | None = pydantic.Field(default=None, alias=str("to-ports"))


class IpFirewallFilterAction(str, enum.Enum):
    """
    Ip firewall filter actions supported by routeros
    """

    Accept = "accept"
    AddDstToAddressList = "add-dst-to-address-list"
    AddSrcToAddressList = "add-src-to-address-list"
    Drop = "drop"
    FasttrackConnection = "fasttrack-connection"
    Jump = "jump"
    Log = "log"
    Passthrough = "passthrough"
    Reject = "reject"
    Return = "return"
    Tarpit = "tarpit"


class IpFirewallFilter(BaseModel):
    """
    Definition of an ip firewall filter
    """

    # action to be performed by this firewall filter
    action: IpFirewallFilterAction
    # action-specific address list field
    address_list: str | None = pydantic.Field(default=None, alias=str("address-list"))
    # protocol-specific field representing a source/destination port
    any_port: str | None = pydantic.Field(default=None, alias=str("any-port"))
    # the chain the firewall filter belongs to
    chain: str
    # comment attached to the ip firewall filter
    comment: str = pydantic.Field(default="")
    # flag that dictates whether an ip firewall filter is active
    disabled: bool = pydantic.Field(default=False)
    # dst address for the firewall fitler
    dst_address: str | None = pydantic.Field(default=None, alias=str("dst-address"))
    # dst address list for the firewall fitler
    dst_address_list: str | None = pydantic.Field(
        default=None, alias=str("dst-address-list")
    )
    # protocol-specific field representing a destination port
    dst_port: str | None = pydantic.Field(default=None, alias=str("dst-port"))
    # the id for an ip firewall filter (NOTE: prefixed with '*')
    id: str | None = pydantic.Field(default=None, alias=str(".id"))
    # action-specific jump target
    jump_target: str | None = pydantic.Field(default=None, alias=str("jump-target"))
    # flag that dictates whether filter is logged
    log: bool = pydantic.Field(default=False)
    # log prefix for logged filter
    log_prefix: str = pydantic.Field(default="", alias=str("log-prefix"))
    # protocol for the firewall filter
    protocol: IpFirewallProtocol | None = pydantic.Field(default=None)
    # protocol-specific field representing a source port
    src_port: str | None = pydantic.Field(default=None, alias=str("src-port"))
    # src address for the firewall fitler
    src_address: str | None = pydantic.Field(default=None, alias=str("src-address"))
    # src address list for the firewall fitler
    src_address_list: str | None = pydantic.Field(
        default=None, alias=str("src-address-list")
    )


class IpDnsRecordType(str, enum.Enum):
    """
    Ip record types supported by routeros
    """

    A = "A"
    AAAA = "AAAA"
    CNAME = "CNAME"
    FWD = "FWD"
    MX = "MX"
    NS = "NS"
    NXDOMAIN = "NXDOMAIN"
    SRV = "SRV"
    TXT = "TXT"


class IpDnsRecord(BaseModel):
    """
    All ip records share a base set of fields - this base class is used to define all ip record modules
    """

    # record-specific address field
    address: str | None = pydantic.Field(default=None)
    # record-specific cname field
    cname: str | None = pydantic.Field(default=None)
    # comment attached to the ip dns record
    comment: str = pydantic.Field(default="")
    # flag that dictates whether an ip address record is active
    disabled: bool = pydantic.Field(default=False)
    # record-specific forward to field
    forward_to: str | None = pydantic.Field(default=None, alias=str("forward-to"))
    # the id for an ip address record (NOTE: prefixed with '*')
    id: str | None = pydantic.Field(default=None, alias=str(".id"))
    # rule that dictates whether a dns record matches subdomains
    match_subdomain: bool = pydantic.Field(default=False, alias=str("match-subdomain"))
    # record-specific mx preference field
    mx_preference: int | None = pydantic.Field(default=None, alias=str("mx-preference"))
    # record-specific mx exchange field
    mx_exchange: str | None = pydantic.Field(default=None, alias=str("mx-exchange"))
    # the name of the dns record
    name: str
    # record-specific ns field
    ns: str | None = pydantic.Field(default=None)
    # record-specific srv port field
    srv_port: int | None = pydantic.Field(default=None, alias=str("srv-port"))
    # record-specific srv priority field
    srv_priority: int | None = pydantic.Field(default=None, alias=str("srv-priority"))
    # record-specific srv target field
    srv_target: str | None = pydantic.Field(default=None, alias=str("srv-target"))
    # record-specific srv weight field
    srv_weight: int | None = pydantic.Field(default=None, alias=str("srv-weight"))
    # record-specific text field
    text: str | None = pydantic.Field(default=None)
    # the ttl of the dns record (represented as '1w1d1h1m1s')
    ttl: str
    # the type of the dns record
    type: IpDnsRecordType


class Request:
    """
    Data container for request data
    """

    # defines the tag attached to the request (and subsequent response sentences)
    tag: str
    # defines the words used to construct this request object (without additional words added via `get_sentence()`)
    words: list[str]

    def __init__(self, words: list[str]):
        self.tag = uuid.uuid4().hex
        self.words = words

    def get_sentence(self) -> list[str]:
        """
        Assembles a sentence using the provided words, the generated tag and an empty string to indicate the end of the sentence
        """
        return [*self.words, *to_api_attribute_words({".tag": self.tag}), ""]


class ResponseSentence:
    """
    Represents a sentence read from routeros
    """

    # 'api_attributes' holds additional metadata (e.g., tags)
    api_attributes: dict[str, str]
    # 'attributes' holds the requested response data
    attributes: dict[str, str]
    # defines the type of sentence (!re, !done, !trap)
    type: str

    def __init__(self, type: str):
        self.api_attributes = {}
        self.attributes = {}
        self.type = type


class ResponseStatus(str, enum.Enum):
    """
    Represents the status of a response received for a sent request.

    An 'error' status occurs when any sentence within a response has the '!trap' type
    A 'success' status occurs when a '!done' sentence is received *without* any '!trap' type sentences

    Because a '!done' message needs to be received for a response to be considered complete - status
    alone does not communicate whether a response is finished.
    """

    InProgress = "in-progress"
    Error = "error"
    Success = "success"


class Response:
    """
    Data container for response data.
    """

    # event signaled with a '!done' sentence is received - optimizes polling for status change
    completion_event: asyncio.Event
    # the request attached to this response
    request: Request
    # the sentences received for the request
    sentences: list[ResponseSentence]
    # the status of the request
    status: ResponseStatus

    def __init__(self, request: Request):
        self.completion_event = asyncio.Event()
        self.request = request
        self.sentences = []
        self.status = ResponseStatus.InProgress

    @property
    def tag(self) -> str:
        """
        Returns the request's tag
        """
        return self.request.tag

    def is_complete(self) -> bool:
        """
        Helper method indicating whether the response has been fully received from routeros
        """
        return self.completion_event.is_set()

    async def wait_until_complete(self, timeout: int | None = None):
        """
        Helper method enabling callers to wait until the response has been completely fetched
        from routeros.
        """
        coro = self.completion_event.wait()
        if timeout:
            coro = asyncio.wait_for(coro, timeout)
        return await coro

    def update_with_sentence(self, sentence: ResponseSentence):
        """
        Updates the response with new data obtained from a sentence received from routeros.
        """
        if self.is_complete():
            raise RuntimeError(f"response is complete")
        self.sentences.append(sentence)
        if sentence.type == "!trap":
            self.status = ResponseStatus.Error
        elif sentence.type == "!done":
            if self.status == ResponseStatus.InProgress:
                self.status = ResponseStatus.Success
            self.completion_event.set()

    def cancel(self):
        """
        'Cancels' an in-progress response by adding a fake sentence with an error indicating the response was cancelled.

        The response is then handled as a 'completed' response, and invokes error logic associated with a failed response

        NOTE: Despite the name, this doesn't invoke the 'cancel' routeros api - it cancels the request client-side
        """
        if self.is_complete():
            raise RuntimeError(f"rresponse is complete")
        sentence = ResponseSentence(type="!trap")
        sentence.attributes["message"] = f"response cancelled"
        self.update_with_sentence(sentence)

    def raise_for_error(self):
        """
        Helper method to raise an exception if a completed response returned an error.
        """
        if not self.is_complete():
            raise RuntimeError(f"response in progress")
        if self.status != ResponseStatus.Error:
            return
        raise ResponseError(response=self)

    def get_data(self) -> list[dict]:
        """
        Helper method to return data from all '!re' sentences in a successful request
        """
        if not self.is_complete():
            raise RuntimeError(f"response in progress")
        if not self.status == ResponseStatus.Success:
            raise RuntimeError(f"response not success")
        data = []
        for sentence in self.sentences:
            if sentence.type != "!re":
                continue
            data.append(dict(sentence.attributes))
        return data

    def get_error_data(self) -> list[dict]:
        """
        Helper method to return the data from all '!trap' sentences in a failed request
        """
        if not self.is_complete():
            raise RuntimeError(f"response in progress")
        if not self.status == ResponseStatus.Error:
            raise RuntimeError(f"response not error")
        data = []
        for sentence in self.sentences:
            if sentence.type != "!trap":
                continue
            data.append(dict(sentence.attributes))
        return data


class ResponseError(Exception):
    """
    Represents a response error sent from routeros
    """

    # the response producing this exception
    response: Response

    def __init__(self, response: Response):
        messages = []
        for error_data in response.get_error_data():
            message = error_data.get("message", "unknown error")
            messages.append(message)
        super().__init__(f"response error: {messages}")
        self.response = response


# convenience type holding the output of `asyncio.open_connection`
Stream = tuple[asyncio.StreamReader, asyncio.StreamWriter]


class Connection:
    """
    Low-level interface managing the socket connection to routeros.
    """

    # background tasks that run while the connection is active (e.g., reading data, checking idle timers)
    background_tasks: list[asyncio.Task]
    # event that's signalled when the connection is closed
    closed_event: asyncio.Event
    # the connection host
    host: str
    # time since activity was last detected
    idle_since: datetime.datetime
    # when timeout exceeded, close the open socket
    idle_timeout: datetime.timedelta
    # the password to supply to routeros' /login api
    password: str
    # in-progress responses being actively worked on by the background task
    responses: dict[str, Response]
    # the stream (reader, writer) connected via socket to the host
    stream: Stream | None
    # a lock that protects the critical path around socket opening/closing vs. reuse
    stream_lock: asyncio.Lock
    # the username to supply to routeros' /login api
    username: str

    def __init__(self, host: str, password: str, username: str):
        self.background_tasks = []
        self.closed_event = asyncio.Event()
        self.closed_event.set()
        self.host = host
        self.idle_since = datetime.datetime.now()
        self.idle_timeout = datetime.timedelta(seconds=10)
        self.password = password
        self.responses = {}
        self.stream = None
        self.stream_lock = asyncio.Lock()
        self.username = username

    async def run_background_idle_monitor(self):
        """
        Run loop that checks whether the connection is idle.  If it is, the connection is closed.
        """
        while not self.closed_event.is_set():
            if not await self.is_idle():
                await asyncio.sleep(1.0)
                continue
            logger.debug(f"idle socket detected")
            # use `create_task` here - this coroutine is awaited as part of `close()`
            asyncio.create_task(self.close())
            # break to prevent several `close()` coroutines from being scheduled
            break

    async def run_background_read(self):
        """
        Run loop that reads from the connected data socket while the connection is active
        """
        while not self.closed_event.is_set():
            await self.read()

    async def is_idle(self) -> bool:
        """
        Returns true when the socket has been idle longer than `idle_timeout`
        """
        now = datetime.datetime.now()
        return (now - self.idle_since) >= self.idle_timeout

    async def read(self):
        """
        Reads sentences from the connected socket.

        Notifies waiters when a response has been fully read.
        """
        if self.stream:
            reader, _ = self.stream
            sentence = await read_sentence(reader)
            if sentence is None:
                return
            self.idle_since = datetime.datetime.now()
            tag = sentence.api_attributes.get(".tag")
            if tag is None:
                raise RuntimeError(f"tag not found")
            response = self.responses[tag]
            logger.debug(f"receive response sentence ({tag}) {sentence.type}")
            response.update_with_sentence(sentence)
            if response.is_complete():
                logger.debug(f"receive response ({tag})")
                self.responses.pop(tag)

    async def open(self) -> Stream:
        """
        Ensures that the client creates a single socket connection to routeros
        through which multiple api calls can be made.

        Performs other initialization that requires a connection to be made -
        like authentication and background response processing tasks.
        """
        # use a lock to ensure that only one connection attempt is made
        async with self.stream_lock:
            old_idle_since = self.idle_since
            self.idle_since = datetime.datetime.now()
            logger.debug(f"idle since: {old_idle_since} -> {self.idle_since}")

            if not self.stream:
                logger.debug(f"opening connection")

                # connect
                self.stream = await asyncio.open_connection(host=self.host, port=8728)

                # clear the `closed_event` signal since the connection is re-opening
                self.closed_event.clear()

                # start background tasks
                self.background_tasks = [
                    asyncio.create_task(self.run_background_idle_monitor()),
                    asyncio.create_task(self.run_background_read()),
                ]

                # authenticate with routeros
                try:
                    response = await self.send(
                        "/login",
                        f"=name={self.username}",
                        f"=password={self.password}",
                        stream=self.stream,
                    )
                    response.raise_for_error()
                except Exception as e:
                    # attempt cleanup since login failed
                    # do not await the task (`close()` needs to acquire the `stream_lock`)
                    asyncio.create_task(self.close())
                    raise e

            return self.stream

    async def close(self):
        """
        Closes an open connection.

        Cleans up anything that might have been initialized from a call to `open()`
        """
        async with self.stream_lock:
            # do nothing if `close()` has already been called
            if self.closed_event.is_set():
                return

            logger.debug(f"closing connection")

            # setting this event allows background tasks to gracefully shut down
            self.closed_event.set()

            # ensure background tasks are no longer running
            while self.background_tasks:
                task = self.background_tasks.pop()
                await task

            # close the stream
            if self.stream:
                _, writer = self.stream
                writer.close()
                await writer.wait_closed()
                self.stream = None

            # cancel all in-progress responses
            while self.responses:
                _, response = self.responses.popitem()
                response.cancel()

    async def send(self, *sentence: str, stream: Stream | None = None):
        """
        Sends a request to routeros.

        The 'stream' option should *not* be provided unless this is being called from within `open()`.
        """
        stream = stream or await self.open()
        request = Request(list(sentence))
        response = Response(request)
        self.responses[response.tag] = response
        logger.debug(f"send request ({request.tag}) {request.words[0]}")
        _, writer = stream
        await write_sentence(writer, request.get_sentence())
        await response.wait_until_complete()
        return response


class Client:
    # the underlying connection through which apis will communicate
    connection: Connection

    def __init__(self, *, host: str, password: str, username: str):
        self.connection = Connection(host=host, password=password, username=username)

    async def list_ip_addresses(self) -> list[IpAddress]:
        """
        Lists IP addresses attached to interfaces
        """
        data = {"detail": None}
        response = await self.connection.send(
            "/ip/address/print", *to_attribute_words(data)
        )
        response.raise_for_error()
        model_cls: pydantic.TypeAdapter[IpAddress] = pydantic.TypeAdapter(IpAddress)
        raw = response.get_data()
        data = list(map(model_cls.validate_python, raw))
        return data

    async def add_ip_dns_record(self, ip_dns_record: IpDnsRecord):
        """
        Adds an IPV4 dns record to routeros
        """
        data = ip_dns_record.model_dump(
            by_alias=True, exclude_none=True, exclude={"id"}
        )
        words = ["/ip/dns/static/add", *to_attribute_words(data)]
        response = await self.connection.send(*words)
        response.raise_for_error()
        id = response.sentences[-1].attributes["ret"]
        ip_dns_record.id = id

    async def set_ip_dns_record(self, ip_dns_record: IpDnsRecord):
        """
        Edits an IPV4 dns record to routeros
        """
        data = ip_dns_record.model_dump(
            by_alias=True, exclude_none=True, exclude={"id"}
        )
        data = {"numbers": ip_dns_record.id, **data}
        words = ["/ip/dns/static/set", *to_attribute_words(data)]
        response = await self.connection.send(*words)
        response.raise_for_error()

    async def set_ip_dns_record_comment(self, ip_dns_record: IpDnsRecord, comment: str):
        """
        Sets the comment for an IPV4 dns record
        """
        data = {"numbers": ip_dns_record.id, "comment": comment}
        words = ["/ip/dns/static/comment", *to_attribute_words(data)]
        response = await self.connection.send(*words)
        response.raise_for_error()
        ip_dns_record.comment = comment

    async def delete_ip_dns_record(self, ip_dns_record: IpDnsRecord):
        """
        Deletes an IPV4 dns records registered with routeros by id
        """
        data = {"numbers": ip_dns_record.id}
        words = ["/ip/dns/static/remove", *to_attribute_words(data)]
        response = await self.connection.send(*words)
        response.raise_for_error()

    async def list_ip_dns_records(self) -> list[IpDnsRecord]:
        """
        Lists IPV4 dns records registered with routeros
        """
        data = {"detail": None}
        response = await self.connection.send(
            "/ip/dns/static/print", *to_attribute_words(data)
        )
        response.raise_for_error()
        model_cls: pydantic.TypeAdapter[IpDnsRecord] = pydantic.TypeAdapter(IpDnsRecord)
        raw = response.get_data()
        for item in raw:
            item.setdefault("type", "A")
        data = list(map(model_cls.validate_python, raw))
        return data

    async def list_ip_firewall_filters(self) -> list[IpFirewallFilter]:
        """
        Lists IPV4 firewall filters registered with routeros
        """
        data = {"detail": None}
        response = await self.connection.send(
            "/ip/firewall/filter/print", *to_attribute_words(data)
        )
        response.raise_for_error()
        model_cls: pydantic.TypeAdapter[IpFirewallFilter] = pydantic.TypeAdapter(
            IpFirewallFilter
        )
        raw = response.get_data()
        data = list(map(model_cls.validate_python, raw))
        return data

    async def add_ip_firewall_filter(self, ip_firewall_filter: IpFirewallFilter):
        """
        Adds an IPV4 firewall filter to routeros
        """
        data = ip_firewall_filter.model_dump(
            by_alias=True, exclude_none=True, exclude={"id"}
        )
        words = ["/ip/firewall/filter/add", *to_attribute_words(data)]
        response = await self.connection.send(*words)
        response.raise_for_error()
        id = response.sentences[-1].attributes["ret"]
        ip_firewall_filter.id = id

    async def set_ip_firewall_filter(self, ip_firewall_filter: IpFirewallFilter):
        """
        Edits an IPV4 firewall filter to routeros
        """
        data = ip_firewall_filter.model_dump(
            by_alias=True, exclude_none=True, exclude={"id"}
        )
        data = {"numbers": ip_firewall_filter.id, **data}
        words = ["/ip/firewall/filter/set", *to_attribute_words(data)]
        response = await self.connection.send(*words)
        response.raise_for_error()

    async def set_ip_firewall_filter_comment(
        self, ip_firewall_filter: IpFirewallFilter, comment: str
    ):
        """
        Sets the comment for an IPV4 firewall filter
        """
        data = {"numbers": ip_firewall_filter.id, "comment": comment}
        words = ["/ip/firewall/filter/comment", *to_attribute_words(data)]
        response = await self.connection.send(*words)
        response.raise_for_error()
        ip_firewall_filter.comment = comment

    async def delete_ip_firewall_filter(self, ip_firewall_filter: IpFirewallFilter):
        """
        Deletes an IPV4 firewall filter registered with routeros by id
        """
        data = {"numbers": ip_firewall_filter.id}
        words = ["/ip/firewall/filter/remove", *to_attribute_words(data)]
        response = await self.connection.send(*words)
        response.raise_for_error()

    async def move_ip_firewall_filter(
        self, ip_firewall_filter: IpFirewallFilter, destination: int
    ):
        """
        Moves an IPV4 firewall filter to the specified position
        """
        data = {"numbers": ip_firewall_filter.id, "destination": destination}
        words = ["/ip/firewall/filter/move", *to_attribute_words(data)]
        response = await self.connection.send(*words)
        response.raise_for_error()

    async def list_ip_firewall_nats(self) -> list[IpFirewallNat]:
        """
        Lists IPV4 firewall nats registered with routeros
        """
        data = {"detail": None}
        response = await self.connection.send(
            "/ip/firewall/nat/print", *to_attribute_words(data)
        )
        response.raise_for_error()
        model_cls = IpFirewallNat
        raw = response.get_data()
        data = list(map(model_cls.model_validate, raw))
        return data

    async def add_ip_firewall_nat(self, ip_firewall_nat: IpFirewallNat):
        """
        Adds an IPV4 firewall nat to routeros
        """
        data = ip_firewall_nat.model_dump(
            by_alias=True, exclude_none=True, exclude={"id"}
        )
        words = ["/ip/firewall/nat/add", *to_attribute_words(data)]
        response = await self.connection.send(*words)
        response.raise_for_error()
        id = response.sentences[-1].attributes["ret"]
        ip_firewall_nat.id = id

    async def set_ip_firewall_nat(self, ip_firewall_nat: IpFirewallNat):
        """
        Edits an IPV4 firewall nat to routeros
        """
        data = ip_firewall_nat.model_dump(
            by_alias=True, exclude_none=True, exclude={"id"}
        )
        data = {"numbers": ip_firewall_nat.id, **data}
        words = ["/ip/firewall/nat/set", *to_attribute_words(data)]
        response = await self.connection.send(*words)
        response.raise_for_error()

    async def set_ip_firewall_nat_comment(
        self, ip_firewall_nat: IpFirewallNat, comment: str
    ):
        """
        Sets the comment for an IPV4 firewall nat
        """
        data = {"numbers": ip_firewall_nat.id, "comment": comment}
        words = ["/ip/firewall/nat/comment", *to_attribute_words(data)]
        response = await self.connection.send(*words)
        response.raise_for_error()
        ip_firewall_nat.comment = comment

    async def delete_ip_firewall_nat(self, ip_firewall_nat: IpFirewallNat):
        """
        Deletes an IPV4 firewall nat registered with routeros by id
        """
        data = {"numbers": ip_firewall_nat.id}
        words = ["/ip/firewall/nat/remove", *to_attribute_words(data)]
        response = await self.connection.send(*words)
        response.raise_for_error()

    async def move_ip_firewall_nat(
        self, ip_firewall_nat: IpFirewallNat, destination: int
    ):
        """
        Moves an IPV4 firewall nat to the specified position
        """
        data = {"numbers": ip_firewall_nat.id, "destination": destination}
        words = ["/ip/firewall/nat/move", *to_attribute_words(data)]
        response = await self.connection.send(*words)
        response.raise_for_error()

    async def list_ip_firewall_address_lists(self) -> list[IpFirewallAddressList]:
        """
        Lists IPV4 firewall address lists registered with routeros
        """
        data = {"detail": None}
        response = await self.connection.send(
            "/ip/firewall/address-list/print", *to_attribute_words(data)
        )
        response.raise_for_error()
        model_cls = IpFirewallAddressList
        raw = response.get_data()
        data = list(map(model_cls.model_validate, raw))
        return data

    async def add_ip_firewall_address_list(
        self, ip_firewall_address_list: IpFirewallAddressList
    ):
        """
        Adds an IPV4 firewall address list to routeros
        """
        data = ip_firewall_address_list.model_dump(
            by_alias=True, exclude_none=True, exclude={"id"}
        )
        words = ["/ip/firewall/address-list/add", *to_attribute_words(data)]
        response = await self.connection.send(*words)
        response.raise_for_error()
        id = response.sentences[-1].attributes["ret"]
        ip_firewall_address_list.id = id

    async def set_ip_firewall_address_list(
        self, ip_firewall_address_list: IpFirewallAddressList
    ):
        """
        Edits an IPV4 dns record to routeros
        """
        data = ip_firewall_address_list.model_dump(
            by_alias=True, exclude_none=True, exclude={"id"}
        )
        data = {"numbers": ip_firewall_address_list.id, **data}
        words = ["/ip/firewall/address-list/set", *to_attribute_words(data)]
        response = await self.connection.send(*words)
        response.raise_for_error()

    async def set_ip_firewall_address_list_comment(
        self, ip_firewall_address_list: IpFirewallAddressList, comment: str
    ):
        """
        Sets the comment for an IPV4 address list
        """
        data = {"numbers": ip_firewall_address_list.id, "comment": comment}
        words = ["/ip/firewall/address-list/comment", *to_attribute_words(data)]
        response = await self.connection.send(*words)
        response.raise_for_error()
        ip_firewall_address_list.comment = comment

    async def delete_ip_firewall_address_list(
        self, ip_firewall_address_list: IpFirewallAddressList
    ):
        """
        Deletes an IPV4 firewall address list registered with routeros by id
        """
        data = {"numbers": ip_firewall_address_list.id}
        words = ["/ip/firewall/address-list/remove", *to_attribute_words(data)]
        response = await self.connection.send(*words)
        response.raise_for_error()


async def write_sentence(writer: asyncio.StreamWriter, sentence: list[str]):
    """
    Helper method to write a setence to a socket connected to the RouterOS API.
    """
    # add an empty write to the sentence to indicate to routeros that the sentence is finished
    for word in sentence:
        await write_word(writer, word)


async def write_word(writer: asyncio.StreamWriter, word: str):
    """
    Writes a word to a socket connected to the RouterOS API.

    Reference: https://help.mikrotik.com/docs/display/ROS/API#API-APIwords
    """
    # encode the length
    # NOTE: this mask is used in `read_word`
    if len(word) <= 0x7F:
        mask = 0x00
        num_bytes = 1
    elif len(word) <= 0x3FFF:
        mask = 0x8000
        num_bytes = 2
    elif len(word) <= 0x1FFFFF:
        mask = 0xC00000
        num_bytes = 3
    elif len(word) <= 0xFFFFFFF:
        mask = 0xE0000000
        num_bytes = 4
    else:
        mask = 0xF000000000
        num_bytes = 5
    encoded_length = (mask | len(word)).to_bytes(num_bytes, "big")

    # assemble the word
    data = encoded_length + word.encode()

    writer.write(data)
    await writer.drain()


async def read_sentence(reader: asyncio.StreamReader) -> ResponseSentence | None:
    """
    Reads a sequence of words from a socket connected to the RouterOS API.

    Returns a sentence object representing the read data
    """
    sentence: ResponseSentence | None = None

    while True:
        word = await read_word(reader)
        if word == "":
            break
        elif word.startswith("!"):
            # read a sentence type - signals the start of a new sentence
            sentence = ResponseSentence(type=word)
        elif sentence and word.startswith("="):
            # read an attribute key/value pair
            parts = word[1:].split("=")
            key, value = parts[0], "=".join(parts[1:])
            sentence.attributes[key] = value
        elif sentence and word.startswith("."):
            # read an api attribute key/value pair
            key, tag = word.split("=")
            sentence.api_attributes[key] = tag
    return sentence


async def read_word(reader: asyncio.StreamReader) -> str:
    """
    Reads a word from a socket connected to the RouterOS API.

    Reference: https://help.mikrotik.com/docs/display/ROS/API#API-APIwords
    """
    # read encoded length
    # NOTE: these values are obtained from the masks in `write_word`
    try:
        header = await asyncio.wait_for(reader.readexactly(1), timeout=1)
    except asyncio.TimeoutError:
        return ""

    # if the byte read is a known header, use it to determine
    # how many bytes need to be read to determine the length
    header = ord(header)
    if header & 0xF0 == 0xF0:
        num_bytes = 4
    elif header & 0xE0 == 0xE0:
        num_bytes = 3
    elif header & 0xC0 == 0xC0:
        num_bytes = 2
    elif header & 0x80 == 0x80:
        num_bytes = 1
    else:
        num_bytes = 0

    if num_bytes:
        # read more data to obtain the length
        data = await reader.readexactly(num_bytes)
        length = ord(data)
    else:
        # the byte read is the length
        length = header

    # read exactly 'length' bytes to obtain data
    data = await reader.readexactly(length)
    return data.decode()


def to_word_value(value: Any) -> str:
    """
    Helper method that converts a value into a valid routeros api word value
    """
    # NOTE: str(None) is 'None', should be ''
    if value is None:
        return ""
    # NOTE: str(bool) -> 'True/False', should be 'true/false'
    if isinstance(value, bool):
        return "true" if value else "false"
    # NOTE: str(<enum>) -> '<EnumClass.VALUE>', should be 'str(<enum>.value)'
    if isinstance(value, enum.Enum):
        return to_word_value(value.value)
    return str(value)


def to_attribute_words(val: dict) -> list[str]:
    """
    Helper method that translates a set of attributes into valid routeros api words
    """
    words = []
    for key, value in val.items():
        words.append(f"={key}={to_word_value(value)}")
    return words


def to_api_attribute_words(val: dict) -> list[str]:
    """
    Helper method that translates a set of api attributes into valid routeros api words

    Ensures that each key is prefixed with '.'
    """
    words = []
    for key, value in val.items():
        if not key.startswith("."):
            raise ValueError(f"key missing . prefix: {key}")
        words.append(f"{key}={to_word_value(value)}")
    return words
