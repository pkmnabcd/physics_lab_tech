from sys import argv
from textwrap import wrap
from os import makedirs

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import lombscargle


def periodicallyRemovePoints(x):
    removeIndices = []
    x_copy = x.tolist()
    for i in range(len(x)):
        if i % 28 == 0:
            j = 0
            while j < 7 and i + j < len(x):
                removeIndices.append(i+j)
                j += 1
    for i in reversed(removeIndices):
        x_copy.pop(i)
    return np.array(x_copy)


if __name__ == "__main__":
    rng = np.random.default_rng()
    nin = 365
    x = np.linspace(1, 365, num=nin)  # Make uniform x array
    x = periodicallyRemovePoints(x)
    print("X vals after removing")
    print(x)

    amp0 = 20
    #amp1 = 100
    freq0 = 0.068
    #freq1 = 0.50
    angFreq0 = 2*np.pi * freq0
    #angFreq1 = 2*np.pi * freq1

    y = amp0*np.cos(angFreq0*x)# + amp1*np.cos(angFreq1*x)

    minFreq = 1 / (x.max() - x.min())
    maxFreq = 0.5 * (1 / np.mean(np.diff(x)))  # Don't ask me why this

    angularFrequencyData = np.linspace(0, 0.6, 1000)   # Makes the list of frequencies to test

    powerData = lombscargle(x, y, angularFrequencyData, normalize=False) # Normalize true vs false is basically the same for this

    angularFrequencyData = angularFrequencyData / (2*np.pi)  # To graph non-angular frequencies

    fig, (ax_t, ax_p) = plt.subplots(2, 1, figsize=(10, 6))

    ax_t.scatter(x, y)
    ax_t.set_xlabel('Time [day]')
    ax_t.set_ylabel('Amplitude')

    ax_p.plot(angularFrequencyData, powerData)
    ax_p.set_xlabel('Frequency [oscillations/day]')
    ax_p.set_ylabel('Power')

    outPath = "test.png"
    plt.savefig(outPath)
    print(f"File saved to {outPath} .")
