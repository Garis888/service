import enum

HTTP_500_TEXT = 'Internal provisioning exception'

GLOBAL_QUEUE = 'global_queqe'

class Status(str, enum.Enum):
    NONE = "NONE"
    RUNNING = "RUNNING"
    COMPLETE = "COMPLETE"
