import libosf as osf 
import numpy as np
#import matplotlib.pyplot as plt

with osf.read_file(r'C:\Users\paj\Desktop\dosto_data_Test\20230905_143856.osf') as f:
    #print([ch.name for ch in f.channels()])
    samples = np.array(f.all_samples())

#plt.plot(samples[1], samples[0])

#plt.show()

print(samples)
