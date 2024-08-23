import numpy as np
import libosf
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt

EXAMPLE_DIR = Path(__file__).absolute().parent
OSF_FILE = EXAMPLE_DIR.joinpath("example.osf")


def find_max():
    with libosf.read_file(OSF_FILE) as f:
        samples: np.ndarray = np.array(f.get_samples(["FuncGen.Sinus"]))
        print(f"length: {samples.shape[1]}")

    plt.plot((samples[1] / 1_000 ** 3).astype(np.datetime64), samples[0])

    plt.show()


find_max()
