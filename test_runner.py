from django.test.runner import DiscoverRunner

class UseDBTestRunner(DiscoverRunner):
    """
    Test runner that looks for an optional DATABASES['TEST']['USEDB'] setting.
    The value of this setting provides the DB name to use for testing.
    """
    def setup_databases(self, **kwargs):
        return setup_databases(
            self.verbosity, self.interactive, self.keepdb, self.debug_sql,
            **kwargs
        )


def setup_databases(verbosity, interactive, keepdb=False, debug_sql=False, parallel=0, **kwargs):
    """    This code is a copy of django.test.utils.setup_databases with a few minor tweaks. """
    from django.test.utils import get_unique_databases_and_mirrors
    from django.db import connections, DEFAULT_DB_ALIAS

    test_databases, mirrored_aliases = get_unique_databases_and_mirrors()

    old_names = []

    for signature, (db_name, aliases) in test_databases.items():
        first_alias = None
        for alias in aliases:
            connection = connections[alias]
            ### J.Fall  The following code block handles the "USEDB" setting
            try:
                usedb = connection.settings_dict['TEST']['USEDB']
                first_alias = alias    # Don't create this DB -- just use the original.
                print('TEST USEDB setting: ', usedb)
            except KeyError:
                pass
            ### ... back to duplicated code...

            old_names.append((connection, db_name, first_alias is None))

            # Actually create the database for the first connection
            if first_alias is None:
                first_alias = alias
                connection.creation.create_test_db(
                    verbosity=verbosity,
                    autoclobber=not interactive,
                    keepdb=keepdb,
                    serialize=connection.settings_dict.get('TEST', {}).get('SERIALIZE', True),
                )
                if parallel > 1:
                    for index in range(parallel):
                        connection.creation.clone_test_db(
                            number=index + 1,
                            verbosity=verbosity,
                            keepdb=keepdb,
                        )
            # Configure all other connections as mirrors of the first one
            else:
                connections[alias].creation.set_as_test_mirror(connections[first_alias].settings_dict)

    # Configure the test mirrors.
    for alias, mirror_alias in mirrored_aliases.items():
        connections[alias].creation.set_as_test_mirror(
            connections[mirror_alias].settings_dict)

    if debug_sql:
        for alias in connections:
            connections[alias].force_debug_cursor = True

    return old_names
