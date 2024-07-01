from commlib.node import Node
from commlib.transports.mqtt import ConnectionParameters
from typing import Any, List, Optional, Tuple
from hbotrc.msgs import (
    StartCommandMessage,
    StopCommandMessage,
    ImportCommandMessage,
    ConfigCommandMessage,
    StatusCommandMessage,
    HistoryCommandMessage,
    BalanceLimitCommandMessage,
    BalancePaperCommandMessage,
    CommandShortcutMessage,
    ExchangeInfoCommandMessage,
    UserDirectedListActiveOrdersCommandMessage,
    UserDirectedTradeCommandMessage,
    UserDirectedCancelCommandMessage,
)
from hbotrc.spec import TopicSpecs


class BotCommands(Node):
    def __init__(self,
                 bot_id: str,
                 host: str = 'localhost',
                 port: int = 1883,
                 username: str = '',
                 password: str = '',
                 namespace: str = 'hbot',
                 **kwargs
                 ):
        self._bot_id = bot_id
        self._ns = namespace

        topic_prefix = TopicSpecs.PREFIX.format(
            namespace=self._ns,
            instance_id=self._bot_id
        )
        self._start_uri = f'{topic_prefix}{TopicSpecs.COMMANDS.START}'
        self._stop_uri = f'{topic_prefix}{TopicSpecs.COMMANDS.STOP}'
        self._import_uri = f'{topic_prefix}{TopicSpecs.COMMANDS.IMPORT}'
        self._config_uri = f'{topic_prefix}{TopicSpecs.COMMANDS.CONFIG}'
        self._status_uri = f'{topic_prefix}{TopicSpecs.COMMANDS.STATUS}'
        self._history_uri = f'{topic_prefix}{TopicSpecs.COMMANDS.HISTORY}'
        self._balance_limit_uri = f'{topic_prefix}{TopicSpecs.COMMANDS.BALANCE_LIMIT}'
        self._balance_paper_uri = f'{topic_prefix}{TopicSpecs.COMMANDS.BALANCE_PAPER}'
        self._command_shortcut_uri = f'{topic_prefix}{TopicSpecs.COMMANDS.COMMAND_SHORTCUT}'
        self._exchange_info_uri = f'{topic_prefix}{TopicSpecs.COMMANDS.EXCHANGE_INFO}'
        self._user_directed_list_active_orders_uri = \
            f'{topic_prefix}{TopicSpecs.COMMANDS.USER_DIRECTED_LIST_ACTIVE_ORDERS}'
        self._user_directed_trade_uri = f'{topic_prefix}{TopicSpecs.COMMANDS.USER_DIRECTED_TRADE}'
        self._user_directed_cancel_uri = f'{topic_prefix}{TopicSpecs.COMMANDS.USER_DIRECTED_CANCEL}'

        conn_params = ConnectionParameters(
            host=host,
            port=int(port),
            username=username,
            password=password
        )

        super().__init__(
            node_name=f'{self._ns}.{self._bot_id}',
            connection_params=conn_params,
            heartbeats=False,
            debug=True,
            **kwargs
        )
        self._init_clients()
        self.run()

    def _init_clients(self):
        self._start_cmd = self.create_rpc_client(
            msg_type=StartCommandMessage,
            rpc_name=self._start_uri
        )
        self._stop_cmd = self.create_rpc_client(
            msg_type=StopCommandMessage,
            rpc_name=self._stop_uri
        )
        self._import_cmd = self.create_rpc_client(
            msg_type=ImportCommandMessage,
            rpc_name=self._import_uri
        )
        self._config_cmd = self.create_rpc_client(
            msg_type=ConfigCommandMessage,
            rpc_name=self._config_uri
        )
        self._status_cmd = self.create_rpc_client(
            msg_type=StatusCommandMessage,
            rpc_name=self._status_uri
        )
        self._history_cmd = self.create_rpc_client(
            msg_type=HistoryCommandMessage,
            rpc_name=self._history_uri
        )
        self._balance_limit_cmd = self.create_rpc_client(
            msg_type=BalanceLimitCommandMessage,
            rpc_name=self._balance_limit_uri
        )
        self._balance_paper_cmd = self.create_rpc_client(
            msg_type=BalancePaperCommandMessage,
            rpc_name=self._balance_paper_uri
        )
        self._command_shortcut_cmd = self.create_rpc_client(
            msg_type=CommandShortcutMessage,
            rpc_name=self._command_shortcut_uri
        )
        self._exchange_info_cmd = self.create_rpc_client(
            msg_type=ExchangeInfoCommandMessage,
            rpc_name=self._exchange_info_uri
        )
        self._user_directed_list_active_orders_cmd = self.create_rpc_client(
            msg_type=UserDirectedListActiveOrdersCommandMessage,
            rpc_name=self._user_directed_list_active_orders_uri
        )
        self._user_directed_trade_cmd = self.create_rpc_client(
            msg_type=UserDirectedTradeCommandMessage,
            rpc_name=self._user_directed_trade_uri
        )
        self._user_directed_cancel_cmd = self.create_rpc_client(
            msg_type=UserDirectedCancelCommandMessage,
            rpc_name=self._user_directed_cancel_uri
        )

    def start(self,
              log_level: str = None,
              script: str = None,
              conf: str = None,
              async_backend: bool = False,
              timeout: int = 5
              ):
        resp = self._start_cmd.call(
            msg=StartCommandMessage.Request(
                log_level=log_level,
                script=script,
                conf=conf,
                async_backend=async_backend
            ),
            timeout=timeout
        )
        return resp

    def stop(self,
             skip_order_cancellation: bool = False,
             async_backend: bool = False,
             timeout: int = 5
             ):
        resp = self._stop_cmd.call(
            msg=StopCommandMessage.Request(
                skip_order_cancellation=skip_order_cancellation,
                async_backend=async_backend
            ),
            timeout=timeout
        )
        return resp

    def import_strategy(self,
                        strategy: str,
                        timeout: int = 5
                        ):
        resp = self._import_cmd.call(
            msg=ImportCommandMessage.Request(strategy=strategy),
            timeout=timeout
        )
        return resp

    def config(self,
               params: List[Tuple[str, Any]],
               timeout: int = 5
               ):
        resp = self._config_cmd.call(
            msg=ConfigCommandMessage.Request(params=params),
            timeout=timeout
        )
        return resp

    def status(self,
               async_backend: bool = False,
               timeout: int = 5
               ):
        resp = self._status_cmd.call(
            msg=StatusCommandMessage.Request(async_backend=async_backend),
            timeout=timeout
        )
        return resp

    def history(self,
                async_backend: bool = False,
                timeout: int = 5
                ):
        resp = self._history_cmd.call(
            msg=HistoryCommandMessage.Request(async_backend=async_backend),
            timeout=timeout
        )
        return resp

    def balance_limit(self,
                      exchange: str,
                      asset: str,
                      amount: float,
                      timeout: int = 5
                      ):
        resp = self._balance_limit_cmd.call(
            msg=BalanceLimitCommandMessage.Request(
                exchange=exchange,
                asset=asset,
                amount=amount
            ),
            timeout=timeout
        )
        return resp

    def balance_paper(self,
                      asset: str,
                      amount: float,
                      timeout: int = 5
                      ):
        resp = self._balance_paper_cmd.call(
            msg=BalancePaperCommandMessage.Request(
                asset=asset,
                amount=amount
            ),
            timeout=timeout
        )
        return resp

    def shortcut(self,
                 params=List[List[Any]],
                 timeout: int = 5
                 ):
        resp = self._command_shortcut_uri.call(
            msg=CommandShortcutMessage.Request(
                params=params
            ),
            timeout=timeout
        )
        return resp

    def exchange_info(
            self,
            exchange: Optional[str] = None,
            timeout: int = 5
    ) -> ExchangeInfoCommandMessage.Response:
        resp = self._exchange_info_cmd.call(
            msg=ExchangeInfoCommandMessage.Request(exchange=exchange),
            timeout=timeout
        )
        return resp

    def user_directed_list_active_orders(
            self,
            exchange: Optional[str],
            trading_pair: Optional[str],
            timeout: int = 5
    ) -> UserDirectedListActiveOrdersCommandMessage.Response:
        resp = self._user_directed_list_active_orders_cmd.call(
            msg=UserDirectedListActiveOrdersCommandMessage.Request(
                exchange=exchange,
                trading_pair=trading_pair,
            ),
            timeout=timeout
        )
        return resp

    def user_directed_trade(
            self,
            exchange: str,
            trading_pair: str,
            is_buy: bool,
            is_limit_order: bool,
            limit_price: Optional[str],
            amount: str,
            timeout: int = 20
    ) -> UserDirectedTradeCommandMessage.Response:
        resp = self._user_directed_trade_cmd.call(
            msg=UserDirectedTradeCommandMessage.Request(
                exchange=exchange,
                trading_pair=trading_pair,
                is_buy=is_buy,
                is_limit_order=is_limit_order,
                limit_price=limit_price,
                amount=amount
            ),
            timeout=timeout
        )
        return resp

    def user_directed_cancel(
            self,
            order_id: str,
            timeout: int = 5
    ) -> UserDirectedCancelCommandMessage.Response:
        resp = self._user_directed_cancel_cmd.call(
            msg=UserDirectedCancelCommandMessage.Request(order_id=order_id),
            timeout=timeout
        )
        return resp
