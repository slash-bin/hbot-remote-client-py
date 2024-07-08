from typing import Any, List, Optional, Tuple, Dict
from commlib.msg import PubSubMessage, RPCMessage, HeartbeatMessage   # noqa: F401
from pydantic import validator, BaseModel
import datetime


class BROKER_STATUS_CODE:
    ERROR: int = 400
    SUCCESS: int = 200


class NotifyMessage(PubSubMessage):
    seq: Optional[int] = 0
    timestamp: Optional[int] = -1
    msg: Optional[str] = ''


class EventMessage(PubSubMessage):
    timestamp: Optional[int] = -1
    type: Optional[str] = 'Unknown'
    data: Optional[Dict[str, Any]] = {}


class LogMessage(PubSubMessage):
    timestamp: Optional[float] = 0.0
    msg: Optional[str] = ''
    level_no: Optional[int] = 0
    level_name: Optional[str] = ''
    logger_name: Optional[str] = ''


class StartCommandMessage(RPCMessage):
    class Request(RPCMessage.Request):
        log_level: Optional[str] = None
        script: Optional[str] = None
        conf: Optional[str] = None
        is_quickstart: Optional[bool] = False
        async_backend: Optional[bool] = False

    class Response(RPCMessage.Response):
        status: Optional[int] = BROKER_STATUS_CODE.SUCCESS
        msg: Optional[str] = ''


class StopCommandMessage(RPCMessage):
    class Request(RPCMessage.Request):
        skip_order_cancellation: Optional[bool] = False
        async_backend: Optional[bool] = False

    class Response(RPCMessage.Response):
        status: Optional[int] = BROKER_STATUS_CODE.SUCCESS
        msg: Optional[str] = ''


class ConfigCommandMessage(RPCMessage):
    class Request(RPCMessage.Request):
        params: Optional[List[Tuple[str, Any]]] = []

    class Response(RPCMessage.Response):
        changes: Optional[List[Tuple[str, Any]]] = []
        config: Optional[Dict[str, Any]] = {}
        status: Optional[int] = BROKER_STATUS_CODE.SUCCESS
        msg: Optional[str] = ''


class CommandShortcutMessage(RPCMessage):
    class Request(RPCMessage.Request):
        params: Optional[List[List[Any]]] = []

    class Response(RPCMessage.Response):
        success: Optional[List[bool]] = []
        status: Optional[int] = BROKER_STATUS_CODE.SUCCESS
        msg: Optional[str] = ''


class ImportCommandMessage(RPCMessage):
    class Request(RPCMessage.Request):
        strategy: str

    class Response(RPCMessage.Response):
        status: Optional[int] = BROKER_STATUS_CODE.SUCCESS
        msg: Optional[str] = ''


class StatusCommandMessage(RPCMessage):
    class Request(RPCMessage.Request):
        async_backend: Optional[bool] = True

    class Response(RPCMessage.Response):
        status: Optional[int] = BROKER_STATUS_CODE.SUCCESS
        msg: Optional[str] = ''
        data: Optional[Any] = ''


class HistoryCommandMessage(RPCMessage):
    class Request(RPCMessage.Request):
        days: Optional[float] = 0
        verbose: Optional[bool] = False
        precision: Optional[int] = None
        async_backend: Optional[bool] = True

    class Response(RPCMessage.Response):
        status: Optional[int] = BROKER_STATUS_CODE.SUCCESS
        msg: Optional[str] = ''
        trades: Optional[List[Any]] = []


class BalanceLimitCommandMessage(RPCMessage):
    class Request(RPCMessage.Request):
        exchange: str
        asset: str
        amount: float

    class Response(RPCMessage.Response):
        status: Optional[int] = BROKER_STATUS_CODE.SUCCESS
        msg: Optional[str] = ''
        data: Optional[str] = ''


class BalancePaperCommandMessage(RPCMessage):
    class Request(RPCMessage.Request):
        asset: str
        amount: float

    class Response(RPCMessage.Response):
        status: Optional[int] = BROKER_STATUS_CODE.SUCCESS
        msg: Optional[str] = ''
        data: Optional[str] = ''


class ExternalEvent(PubSubMessage):
    name: str
    timestamp: Optional[int] = -1
    sequence: Optional[int] = 0
    type: Optional[str] = 'eevent'
    data: Optional[Dict[str, Any]] = {}

    @validator('timestamp', pre=True, always=True)
    def set_ts_now(cls, v):
        return v or datetime.now().timestamp()


class ExchangeInfo(BaseModel):
    name: str
    trading_pairs: List[str]
    balances: Dict[str, float]


class ExchangeInfoCommandMessage(RPCMessage):
    class Request(RPCMessage.Request):
        exchange: Optional[str]

    class Response(RPCMessage.Response):
        status: Optional[int] = BROKER_STATUS_CODE.SUCCESS
        exchanges: List[ExchangeInfo] = []
        msg: str = ''


class UserDirectedTradeCommandMessage(RPCMessage):
    class Request(RPCMessage.Request):
        exchange: str
        trading_pair: str
        is_buy: bool
        is_limit_order: bool
        limit_price: Optional[str]
        amount: str

    class Response(RPCMessage.Response):
        status: Optional[int] = BROKER_STATUS_CODE.SUCCESS
        order_id: str = ''
        msg: str = ''


class UserDirectedCancelCommandMessage(RPCMessage):
    class Request(RPCMessage.Request):
        order_id: str

    class Response(RPCMessage.Response):
        status: Optional[int] = BROKER_STATUS_CODE.SUCCESS
        exchange: str = ''
        trading_pair: str = ''
        order_id: str = ''
        msg: str = ''


class OpenOrderInfo(BaseModel):
    exchange: str
    trading_pair: str
    order_id: str
    is_buy: bool
    is_limit_order: bool
    limit_price: Optional[str]
    amount_total: str
    amount_remaining: str
    order_state: str
    msg: Optional[str]


class UserDirectedListActiveOrdersCommandMessage(RPCMessage):
    class Request(RPCMessage.Request):
        exchange: Optional[str] = None
        trading_pair: Optional[str] = None

    class Response(RPCMessage.Response):
        status: Optional[int] = BROKER_STATUS_CODE.SUCCESS
        active_orders: List[OpenOrderInfo]
        msg: str = ''


class UserDirectedOrderUpdateMessage(PubSubMessage):
    timestamp: Optional[int] = -1
    exchange: str
    trading_pair: str
    is_buy: bool
    is_limit_order: bool
    limit_price: Optional[str]
    amount_total: str
    amount_remaining: str
    order_state: str
    msg: str = ''
