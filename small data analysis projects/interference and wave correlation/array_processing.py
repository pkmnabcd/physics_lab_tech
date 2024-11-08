import numpy as np
import matplotlib.pyplot as plt


def monthly_interference_count(df):
    MONTH_STUBS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    out_list = []

    for stub in MONTH_STUBS:
        month_interference_count = 0
        for i in range(len(df)):
            if stub in df['date'][i]:
                if float(df['interference?'][i]) >= .4:
                    month_interference_count += 1
        out_list.append(month_interference_count)
    return out_list


def monthly_days_with_waves_count(df):
    MONTH_STUBS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    out_list = []

    for stub in MONTH_STUBS:
        month_wave_count = 0
        for i in range(len(df)):
            if stub in df['date'][i]:
                month_wave_count += int(df['possible wave?'][i])
        out_list.append(month_wave_count)
    return out_list


def make_graph(interference_data, waves_data, year):
    months = np.array(["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                   "November", "December"])
    interference, waves = np.array(interference_data), np.array(waves_data)

    COLOR_INTERFERENCE = 'r'
    COLOR_WAVES = "#3399e6"

    fig, ax1 = plt.subplots(figsize=(15, 7))
    ax2 = ax1.twinx()

    ax1.plot(months, interference, color=COLOR_INTERFERENCE, marker='o', label="Interference")
    ax2.plot(months, waves, color=COLOR_WAVES, marker='o', label="Waves")

    ax1.set_xlabel("Month")
    ax1.set_ylabel("Number of Days with Debilitating Interference", color=COLOR_INTERFERENCE)
    ax2.set_ylabel("Number of Days with Waves Present", color=COLOR_WAVES)

    ax1.set_ylim(0, 28)
    ax2.set_ylim(0, 28)

    ax1.grid(visible=True, axis='both')
    ax1.legend(loc=2)
    ax2.legend(loc=0)
    fig.suptitle(year, fontsize=15)

    plt.show()
