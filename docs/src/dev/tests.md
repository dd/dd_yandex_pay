# Tests

The project uses [pytest](https://docs.pytest.org/) for testing, as well as set up coverage tests using [pytest-cov](https://pytest-cov.readthedocs.io/), it is highly recommended for review.


## Usage

You can run tests in a development environment with the following command:

```console
$ hatch run test:check
```

A matrix for a set of python and django versions is also configured in hatch, you can see more about this in the settings in the `pyproject.toml` file, you can run the entire test matrix with the hatch script:

```console
$ hatch run mtest:check
```


## Autotests

Tests are automatically processed when pushing to `main`, `dev` and release branches `release/*`. See workflow [config](https://github.com/dd/dd_yandex_pay/blob/main/.github/workflows/test.yml) for details.

In the process, test results are uploaded to [codecov.io](https://app.codecov.io/gh/dd/dd_yandex_pay).
