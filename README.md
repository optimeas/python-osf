# Python OSF Implementation 

Package to read in data from OSF files.
Supported OSF version:

    - OSF4

## Usage

See `./examples/` 

## Common commands for development tasks

### Install editable development installation

``` shell
  # install local development version
  cd libosf/
  pip install -e .
```

### Run unit tests
``` shell
  # install dependencies
  cd libosf/
  pip install .[tests]
  # run python unit tests
  pytest
```

### Build HTML documentation

``` shell
  # install dependencies
  cd libosf/
  pip install .[docs]
  # build the html documentation
  cd docs
  sphinx-build source/ build/ 
```

