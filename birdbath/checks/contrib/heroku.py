import os
from birdbath.checks import BaseCheck


class HerokuNotProductionCheck(BaseCheck):
    def check(self):
        heroku_app_name = os.environ.get("HEROKU_APP_NAME")
        return heroku_app_name and "production" not in heroku_app_name
