import shapely
import os
import environ
print("d")
if settings.DEBUG:
    environ.read_env()
else:
    api_key = os.environ.get(