# django-usedb-testrunner
A custom Django test runner that runs tests against an existing DB

**Use Case**:  Specify the DB to run tests against.   
For example, use a legacy DB (un-managed), 
or a read-only DB where it is un-important to test creation, 
but important to test connection, trigger functions, and that models match schema.

**Usage**:  in setting:

`TEST_RUNNER = 'your_app.test_runner.UseDBTestRunner' `


## Approach
1. Hardcode the `--keepdb` option - ensures django test machinery does not destroy DB
2. Set `DATABASES[alias][TEST][NAME] = DATABASES[alias][NAME]` - force use of settings.DATABASE

**Why?**

You can emulate this behaviour by setting the DB `[TEST][NAME]` in settings and running tests
with `--keepdb` option.  BUT there is a risk of data loss -- if test get run without `--keepdb`, 
django's test machinery may delete you Database!!  

This simple test runner prevents this potential harm be ensuring both settings work together.