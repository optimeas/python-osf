import numpy as np 
import libosf
from datetime import datetime
import matplotlib.pyplot as plt
filename = r'.\Desktop\mydata.osf'

def find_max():
    with libosf.read_file(filename) as f:
        samples = np.array(f.get_samples_by_name(['CAN1.ADC104']))

    plt.plot((samples[1] / 1_000 ** 3).astype(np.datetime64), samples[0])

    plt.show()

find_max()

