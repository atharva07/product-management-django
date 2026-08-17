from rest_framework.throttling import UserRateThrottle

class LowStockThrottle(UserRateThrottle):
    scope = "low_stock"