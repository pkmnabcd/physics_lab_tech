from sys import argv
from textwrap import wrap
from os import makedirs

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import lombscargle





if __name__ == "__main__":
    rng = np.random.default_rng()
    nin = 360
    x = rng.uniform(0, 16*np.pi, nin)

    amp0 = 40
    freq0 = 0.5
    angFreq0 = 2*np.pi * freq0

    y = amp0*np.cos(angFreq0*x)
    minFreq = 1 / (x.max() - x.min())
    maxFreq = 0.5 * (1 / np.mean(np.diff(x)))  # Don't ask me why this

    angularFrequencyData = np.linspace(minFreq / 2, maxFreq * 1.5, 1000)
    powerData = lombscargle(x, y, angularFrequencyData, normalize=False)


    fig, (ax_t, ax_p, ax_n, ax_a) = plt.subplots(4, 1, figsize=(5, 6))

    ax_t.plot(x, y)
    ax_t.set_xlabel('Time [s]')
    ax_t.set_ylabel('Amplitude')

    ax_t.plot(angularFrequencyData, powerData)
    ax_p.set_xlabel('Angular frequency [rad/s]')
    ax_p.set_ylabel('Power')
