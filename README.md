# Python OSF Implementation

Package to read in data from OSF files.
Supported OSF versions:

- OSF4
## Installation

Setting up a virtual environment and installing the current master:

Windows:

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install .
```

Linux:

```bash
python -m venv venv
. ./venv/bin/activate
pip install .
```

## Usage

Constructing a dataframe with the samples of two channels of an OSF file:

```python
from libosf import read_file
import pandas as pd

channels = ['System.CPU.Uptime', 'System.Device.AppUptime']

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
cd examples/
# generates a csv file with samples of "System.CPU.Uptime" at example.csv
python to_csv.py -i example.osf -c System.CPU.Uptime
```

## Common commands for development tasks

### Install editable development installation

```shell
  # install local development version
  pip install -e .
```

### Run unit tests
```shell
  # install dependencies
  pip install .[tests]
  # run python unit tests
  pytest
```

### Build HTML documentation

``` shell
  # install dependencies
  pip install .[docs]
  # build the html documentation
  cd docs/
  sphinx-build source/ build/html/

  # Alternatively, if "make" is available:
  make html
```

