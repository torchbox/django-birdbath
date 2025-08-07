import os

from birdbath.checks import BaseCheck


class HerokuNotProductionCheck(BaseCheck):
    def check(self):
        heroku_app_name = os.environ.get("HEROKU_APP_NAME")
        if not heroku_app_name: 
            # When the variable is not set, we are not on Heroku.
            return true
        if "production" in heroku_app_name:
            # If the variable is set and contains "production" we want to fail.
            return false
        return true


class HerokuAnonymisationAllowedCheck(BaseCheck):
    def check(self):
        heroku_app_name = os.environ.get("HEROKU_APP_NAME")
        allows_anonymisation = os.environ.get("ALLOWS_ANONYMISATION")
        return heroku_app_name == allows_anonymisation
