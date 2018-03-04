import os
import functools

# See: https://stackoverflow.com/a/35196369/798575
def pytest_runtest_setup(item):
    """
    Execute each test in the directory where the test file lives.
    """
    starting_directory = os.getcwd()
    test_directory = os.path.dirname(str(item.fspath))
    os.chdir(test_directory)

    teardown = functools.partial(os.chdir, starting_directory)
    # There's probably a cleaner way than accessing a private member.
    item.session._setupstate.addfinalizer(teardown, item)
