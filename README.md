# Python OSF Implementation 

Package to read in data from OSF files.
Supported OSF versions:

- OSF4
## Installation

Setting up a virutal environment and installing the current master:

Windows:

```powershell
cd python-osf4
python -m venv venv
.\venv\Scripts\activate
pip install .
```

## Usage

Constructing a dataframe with the samples of two Channels of a osf file:

```python
from libosf import read_file
import pandas as pd

channels = ['CAN_1', 'CAN_2']

with read_file('example.osf') as file:
    samples = file.get_samples(channels)
    data = {
            'ts_n': samples[0],
            'value': samples[1],
            'ch_index': samples[2]
    }
    df = pd.DataFrame(data=data)
```


## Examples 

More examples showing how to use this package combined with numpy, pandas, matplotlib and more can be found under `./examples/`. 

Install dependencies before running:

```bash
pip install .[examples]
# generates an csv file with CAN_1 samples at python-osf4/output.csv
python examples/to_csv.py -i input.osf -c CAN_1
```
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

