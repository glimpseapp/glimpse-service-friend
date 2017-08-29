import os

GLIMPSE_SERVICE_USER = os.getenv("USER_INFO_BULK_URL", "http://localhost:5000")
USER_INFO_BULK_URL = GLIMPSE_SERVICE_USER + "/users"



