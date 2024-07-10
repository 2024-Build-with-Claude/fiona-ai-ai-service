import enum


class TransactionTypeEnum(enum.Enum):
    """
    Transaction type enum
    """

    GAIN = "gain"
    SPEND = "spend"
