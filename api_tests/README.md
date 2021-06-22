# Api-Tests

This is a collection of end-to-end test suits to verify the oauth api is working as intended.

* `config_files/` This contains all the configuration for running the tests.
* `user_role_shared_flow/` The tests are defined here (this is also where we execute the tests from)

We are using pytest as our test runner, you can find out more about pytest by visiting
the [pytest docs](https://docs.pytest.org/en/latest/).

## Contributing
Contributions to this project are welcome from anyone, providing that they conform to
the [guidelines for contribution](https://github.com/NHSDigital/template-api/blob/master/CONTRIBUTING.md) and
the [community code of conduct](https://github.com/NHSDigital/template-api/blob/master/CODE_OF_CONDUCT.md).

### Licensing
This code is licensed under the MIT license. Any new work added to this repository must conform to the
conditions of this licenses. In particular this means that this project may not depend on GPL-licensed or
AGPL-licensed libraries, as these would violate the terms of those libraries' licenses.

The contents of this repository are protected by Crown Copyright (C).

### Requirements
* python 3.8
* [make](http://gnuwin32.sourceforge.net/packages/make.htm) this comes pre-installed on Linux or Mac.

### Install locally
Navigate to the /api_tests folder and run the commands:
```shell
$ pip install virtualenv
$ virtualenv test_env
$ source ./test_env/bin/activate
(test_env) $ pip install -r requirements.txt
```

### Environment Variables
Before you can start creating and running tests you need to configure all the required environment variables.
See list of required variables below
(these are all described in the config_files/config.py file).

 * `OAUTH_BASE_URI` The base url for the OAuth api e.g 'https://internal-dev.api.service.nhs.uk'
 * `OAUTH_PROXY` The proxy you want to get the tokens from e.g 'oauth2'
 * `JWT_PRIVATE_KEY_ABSOLUTE_PATH` The path to your jwt private key
 * `APIGEE_API_TOKEN` Your personal Apigee token 
 * `ID_TOKEN_PRIVATE_KEY_ABSOLUTE_PATH` The path to your ide_token private key
 * `MOCK_PROXY` = The proxy consuming the shared flow e.g 'mock-nhsid-jwks-pr-12'

NOTE: if you are using Docker you need to fill in the docker.env file with the variable values.


## Pytest basics
 * `quiet mode` --pytest -q
 * `verbose mode` --pytest -v
 * `run a specific test within a module` -- pytest test_mod.py::test_func
 * `run a specific test within a class` -- pytest test_mod.py::TestClass::test_method
 * `by test suite` -- pytest filename.py
 * `keywords` -- pytest -k "KEYWORD" -k "KEYWORD_1 or KEYWORD_2" -k "KEYWORD_1 and KEYWORD_2"
 * `marks` -- pytest -m MARK
 * `stop after first failure` -- pytest -x
 * `display print statements` -- pytest -s


## Running tests
Test can be either executed using a virtual env and from a terminal/command window or from within an IDE (preferably PyCharm). These are explained below.


### Execute locally
In order to run the tests, make sure you have a command window or terminal open and
activate you virtualenv as detailed in setup steps 5 and 6.

Navigate to the api_tests folder and run:

    pytest -v --junitxml=report.xml

This will run the test suite and show the number of failing and passing tests as well as any errors.
Running with the "-v" flag will
run thes tests in verbose mode and it provides additional details (ideal for debugging). The "--junitxml" flag
generates an xml test report in the same directory as the test suite called report.xml. This
will be overwritten with every run. This xml report is only really going to be useful for things
that pick up the report and do something with it, such as jenkins and so the flag is probably
only necessary when running under this context.

To be more specific about the tests that you run, alter the pytest command using the below as
examples:

```shell
# Runs all tests
pytest -v tests/

# Runs specific test file
pytest -v tests/filename.py

# Runs tests in a class in a test file
pytest tests/filename.py::TestClassSuite

# Runs a single test method
pytest tests/filename.py::TestClassSuite::test_method
```

### Running in Pycharm
When developing scripts, it can be incredibly useful to run from inside Pycharm in order to add
breakpoints, debug and follow the code a lot easier etc.

#### Virtual env instance
To set this up, open the project inside the IDE.

1. In the setting menu, select the Project then Project interpreter sub-menu.

2. There is a dropdown box at the top with a small cog button next to it.

3. Click the cog and then add local. Navigate to the folder where your

4. virtualenv is and select the Python.exe from inside the script folder.

This will make sure Pycharm knows to run the tests with the libraries and Python interpreter from the virtualenv.
You should now be able to right click any function/test and run or debug from inside the IDE and
PyCharm features like autocompletion, code inspections, and checks will be driven by this interpreter.


## Developing New Scripts
The test runner pytest will pick up any file which start with "test_*.py". New tests should be created
in these files inside a class that follows the convention 'Test*Suite' and individual tests should be in functions
that start with "test_".

Tests are split into various layers. The top layer is in the tests folder and is any file
ending with '_test'. These call reusable steps from files in the steps folder and perform an
assertion. An assertion merely checks if something is true. Therefore, steps from the test layer
should return True or False. These reusable steps are split into classes which represent an api or a
group of smaller functions of an api.

There is one final layer which are the files located in the scripts folder, there are steps that are
reusable across multiple apis. Here we have a parent Base class that all other api checks would inherit from.

### Marks
Tests can be marked with specific 'marks'. Think of marks as tagging a test with some metadata.
These marks are defined in the pytest.ini file and must be strictly followed
(meaning you can only use the marks that have been predefined).
To create a new mark you simply insert a new line in the pytest.ini file
following the convention: mark_name: mark_description.

### Adding Marks to Tests
You can add one or more marks to a test. To add a mark simply define a decorator to the test.

Example:

```python
@pytest.mark.name_of_mark
@pytest.mark.name_of_another_mark
def test_example():
    assert some_test_method()
```

Example running all the tests that have been marked with the "name_of_mark" mark:

``` shell
pytest -m name_of_mark -v tests/
```
