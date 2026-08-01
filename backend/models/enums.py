import enum

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"
    PRO = "pro"

class ListingStatus(str, enum.Enum):
    ACTIVE = "active"
    SOLD = "sold"
    INACTIVE = "inactive"
    REMOVED = "removed"

class SellerType(str, enum.Enum):
    INDIVIDUAL = "individual"
    DEALER = "dealer"

class ScrapeJobStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class LogLevel(str, enum.Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class TriggerType(str, enum.Enum):
    PRICE_DROP = "price_drop"
    NEW_LISTING = "new_listing"
    SOLD = "sold"
