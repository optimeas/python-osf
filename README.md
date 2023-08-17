# Generic Python Project Template

This is template for quickly setting up python projects. Clone this repository and start developing.

## Checklist to getting started

- Rename the project "example" at the following places:
  - Filepath: src/example
  - Filepath: tests/unit/test_example.py
    - also in the contents of this file replace the import statement
  - Inside pyproject.toml
    - name = "example"
    -  Under [project.scripts]
- Replace the contents of this README.md with a project description
- Replace the values inside the sphinx documentation configuration `docs/source/conf.py`

## Common commands for development tasks

### Install local development installation

``` shell
  # install local development version
  cd generic-python-project/
  pip install -e .
  # execute a example script
  example
  # see below for more examples for development tasks
```

### Run unit tests
``` shell
  # install dependencies
  cd generic-python-project/
  pip install .[tests]
  # run python unit tests
  pytest
  # run robot acceptance tests and automation tasks
  robot .
```

### Build HTML documentation

``` shell
  # install dependencies
  cd generic-python-project/
  pip install .[docs]
  # build the html documentation
  cd docs
  sphinx-build source/ build/ 
```

