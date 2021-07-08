"""
Test runner that uses the DB in settings (does not create test DB)
 -- caution - tests run against data in the DB and may leave spurious data in that DB!
Approach:
 - keepdb == True  :  prevents normal logic that creates / destroys DB from kicking in
 - set name of test DB to the settings.DATABASE name so runner sees DB already exists
"""
from django.conf import settings
from django.db import connections
from django.test.runner import DiscoverRunner

class UseDBTestRunner(DiscoverRunner):
    """
    Test runner that prevents create / destroy of test DB, using the DB defined in settings instead.
    """
    def _force_test_db_names(self):
        for alias in connections:
            connection = connections[alias]
            db_name = settings.DATABASES[alias]["NAME"]
            settings.DATABASES[alias]['TEST']["NAME"] = db_name
            settings.DATABASES[alias]['TEST']["SERIALIZE"] = False
            settings.DATABASES[alias]['TEST']["MIGRATE"] = False
            connection.settings_dict["NAME"] = db_name
            connection.settings_dict['TEST'] = settings.DATABASES[alias]['TEST']


    def setup_databases(self, **kwargs):
        self.keepdb = True
        self._force_test_db_names()
        return super().setup_databases(**kwargs)
