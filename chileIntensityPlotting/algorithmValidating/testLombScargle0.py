from sys import argv
from textwrap import wrap
from os import makedirs

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import lombscargle


def sort_arrays_together(x, y):
    if len(x) != len(y):
        print("Error: Arrays x and y must have the same length.")
        return [], []

    sorted_indices = np.argsort(x)
    sorted_x = x[sorted_indices]
    reordered_y = y[sorted_indices]

    return sorted_x, reordered_y


if __name__ == "__main__":
    rng = np.random.default_rng()
    nin = 150
    x = rng.uniform(0, 20*np.pi, nin)

    amp0 = 40
    freq0 = 0.20
    angFreq0 = 2*np.pi * freq0

    y = amp0*np.cos(angFreq0*x)
    x, y = sort_arrays_together(x,y)

    minFreq = 1 / (x.max() - x.min())
    maxFreq = 0.5 * (1 / np.mean(np.diff(x)))  # Don't ask me why this

    angularFrequencyData = np.linspace(minFreq / 2, maxFreq * 1.5, 1000)


    powerData = lombscargle(x, y, angularFrequencyData, normalize=False)

    angularFrequencyData = angularFrequencyData / (2*np.pi)

    fig, (ax_t, ax_p) = plt.subplots(2, 1, figsize=(8, 6))

    ax_t.scatter(x, y)
    ax_t.set_xlabel('Time [s]')
    ax_t.set_ylabel('Amplitude')

    ax_p.plot(angularFrequencyData, powerData)
    ax_p.set_xlabel('Frequency [oscillations/s]')
    ax_p.set_ylabel('Power')

    outPath = "test.png"
    plt.savefig(outPath)
    print(f"File saved to {outPath} .")
