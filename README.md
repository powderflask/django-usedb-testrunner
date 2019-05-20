# django-usedb-testrunner
A custom Django test runner that runs tests against an existing DB

**Use Case**:  Specify the DB to run tests against.   For example, use a legacy DB (un-managed), or a read-only DB where it is un-important to test creation, but important to test connection, trigger functions, and that models match schema.

**Usage**:  in DATABASES setting, add:

    'TEST' :{
        'USEDB': 'your_test_DB_name_here',
    }

and setting:
`TEST_RUNNER = 'your_app.test_runner.UseDBTestRunner' `
