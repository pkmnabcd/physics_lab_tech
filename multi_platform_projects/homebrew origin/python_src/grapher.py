import matplotlib.pyplot as plt


class CombinedGraph:
    def __init__(self, datasets: dict, metadata: dict, x_axis: list):
        self.metadata = metadata
        self.x_axis = x_axis

        self.P12_data = datasets["P12"]
        self.P14_data = datasets["P14"]
        self.BG_data = datasets["BG"]
        self.Dark_data = datasets["ActDark"]

        self.OH_temp_data = datasets["OHTemp"]
        self.OH_band_data = datasets["OHBandInt"]
        self.CCD_temp_data = datasets["CCDTemp"]

        self.fig = self.axes = None

    def generate_graph(self):
        # Create a figure with 2 rows and 2 columns of subplots
        self.fig, self.axes = plt.subplots(2, 2, figsize=(20, 12))

        filter_plot = self.axes[0, 0]
        OHTemp_plot = self.axes[0, 1]
        OHBand_plot = self.axes[1, 0]
        CCDTemp_plot = self.axes[1, 1]

        filter_plot.plot(self.x_axis, self.P12_data, label="P12")
        filter_plot.plot(self.x_axis, self.P14_data, label="P14")
        filter_plot.plot(self.x_axis, self.BG_data, label="BG")
        filter_plot.plot(self.x_axis, self.Dark_data, label="ActDark")

        OHTemp_plot.plot(self.x_axis, self.OH_temp_data, label="OHTemp")
        OHBand_plot.plot(self.x_axis, self.OH_band_data, label="OHBand")
        CCDTemp_plot.plot(self.x_axis, self.CCD_temp_data, label="CCDTemp")

        x_label = "UT Time (hr)"

        filter_plot.set_ylabel("Intensity (counts)", fontsize=20)
        OHTemp_plot.set_ylabel("Temperature (K)", fontsize=20)
        OHBand_plot.set_ylabel("Band Intensity (counts)", fontsize=20)
        CCDTemp_plot.set_ylabel("°C", fontsize=20)

        doy = self.metadata["day_of_year"]
        year = self.metadata["year"]
        date = self.metadata["date"]
        self.fig.suptitle(f"ALO, Chile\nUT Day {doy} {year} (LT {date} δt = -4 hrs)", fontsize=20)

        for ax in self.axes.flat:
            ax.legend(fontsize=16)
            ax.set_xlabel(x_label, fontsize=20)
            ax.tick_params(labelsize=16)

        plt.tight_layout()  # Adjust spacing between plots

    def save_graph(self, save_dir):
        save_path = save_dir

        year = self.metadata["year"]
        date = self.metadata["date"]
        filename = f"{date}_{year}.png"
        if self.metadata["edited"]:
            filename = f"{date}_{year}e.png"
        save_path += filename

        print(f"Saving {filename} to {save_path}")
        self.fig.savefig(save_path)
