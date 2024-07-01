
class CommandTopicSpecs:
    START: str = '/start'
    STOP: str = '/stop'
    CONFIG: str = '/config'
    IMPORT: str = '/import'
    STATUS: str = '/status'
    HISTORY: str = '/history'
    BALANCE_LIMIT: str = '/balance/limit'
    BALANCE_PAPER: str = '/balance/paper'
    COMMAND_SHORTCUT: str = '/command_shortcuts'
    EXCHANGE_INFO: str = '/exchange_info'
    USER_DIRECTED_TRADE: str = '/user_directed/trade'
    USER_DIRECTED_CANCEL: str = '/user_directed/cancel'
    USER_DIRECTED_LIST_ACTIVE_ORDERS: str = '/user_directed/list_active_orders'


class TopicSpecs:
    PREFIX: str = '{namespace}/{instance_id}'
    COMMANDS: CommandTopicSpecs = CommandTopicSpecs()
    LOGS: str = '/log'
    MARKET_EVENTS: str = '/events'
    NOTIFICATIONS: str = '/notify'
    HEARTBEATS: str = '/hb'
    EXTERNAL_EVENTS: str = '/external/event/*'
