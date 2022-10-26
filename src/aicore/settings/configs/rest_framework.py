REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.NamespaceVersioning",
    "EXPIRED_FOREVER": "2000-10-10 00:00:00",
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    "DEFAULT_THROTTLE_RATES": {
        "custom_user": "180/minutes",
        "email_unsubscribe": "10/day",
        "hourly_requests": "12/day",
        "auth_hourly_requests": "6/hour",
        "webhook_per_min_requests_by_sms": "15/minute",
        "webhook_per_min_requests_by_ip": "240/minute",
        "checkr_hourly": "1/hour",
        "location_per_hour": "10/hour"
    },
    "OVERRIDE_THROTTLE_RATES": {"special": "10000/hour"},
    # "DEFAULT_CONTENT_NEGOTIATION_CLASS": ""
}

REST_FRAMEWORK_CACHE = {
    "DEFAULT_CACHE_TIMEOUT": 86400,  # 24 * 60 * 60
}
