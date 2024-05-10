import matplotlib.pyplot as plt
# Useful website: https://stackoverflow.com/questions/11159436/multiple-figures-in-a-single-window


class SingleGraph:
    def __init__(self, datasets: dict):
        if type(self) is SingleGraph:
            raise NotImplementedError("SingleGraph is an abstract class and must be extended")
        self.datasets = datasets


class SingleGraph1Set(SingleGraph):
    def __init__(self, data: list, data_type: str):
        super().__init__({data_type: data})


class SingleGraph4Sets(SingleGraph):
    def __init__(self,
                 data0: list, data_type0: str,
                 data1: list, data_type1: str,
                 data2: list, data_type2: str,
                 data3: list, data_type3: str):
        super().__init__({
            data_type0: data0,
            data_type1: data1,
            data_type2: data2,
            data_type3: data3
        })


class CombinedGraph:
    def __init__(self, graph0: SingleGraph, graph1: SingleGraph,
                 graph2: SingleGraph, graph3: SingleGraph, metadata: dict, x_axis: list):
        self.graph0, self.graph1, self.graph2, self.graph3 = graph0, graph1, graph2, graph3
        self.metadata = metadata
        self.x_axis = x_axis

        self.P12_data = graph0.datasets["P12"]
        self.P14_data = graph0.datasets["P14"]
        self.BG_data = graph0.datasets["BG"]
        self.Dark_data = graph0.datasets["ActDark"]

        self.OH_temp_data = graph1.datasets["OHTemp"]
        self.OH_band_data = graph2.datasets["OHBandInt"]
        self.CCD_temp_data = graph3.datasets["CCDTemp"]

        self.fig = self.axes = None

    def generate_graph(self):
        # Create a figure with 2 rows and 2 columns of subplots
        self.fig, self.axes = plt.subplots(2, 2, figsize=(10, 6))  # Adjust figsize as needed

        filter_plot = self.axes[0, 0]
        OHTemp_plot = self.axes[0, 1]
        OHBand_plot = self.axes[1, 0]
        CCDTemp_plot = self.axes[1, 1]

        filter_plot.plot(self.x_axis, self.P12_data, label="P12")
        filter_plot.plot(self.x_axis, self.P14_data, label="P14")
        filter_plot.plot(self.x_axis, self.BG_data, label="BG")
        filter_plot.plot(self.x_axis, self.Dark_data, label="ActDark")

        OHTemp_plot.plot(self.x_axis, self.OH_temp_data, label="OHTemp")  # TODO: Check with paper copies that the order is right
        OHBand_plot.plot(self.x_axis, self.OH_band_data, label="OHBand")
        CCDTemp_plot.plot(self.x_axis, self.CCD_temp_data, label="CCDTemp")

        x_label = "UT Time (hr)"

        filter_plot.set_ylabel("Intensity (counts)")
        filter_plot.set_xlabel(x_label)
        OHTemp_plot.set_ylabel("Temperature (K)")
        OHTemp_plot.set_xlabel(x_label)
        OHBand_plot.set_ylabel("Band Intensity (counts)")
        OHBand_plot.set_xlabel(x_label)
        CCDTemp_plot.set_ylabel("°C")
        CCDTemp_plot.set_xlabel(x_label)

        doy = self.metadata["day_of_year"]
        year = self.metadata["year"]
        date = self.metadata["date"]
        self.fig.suptitle(f"ALO, Chile\nUT Day {doy} {year} (LT {date} δt = -4 hrs")

        for ax in self.axes.flat:
            ax.legend()

        plt.tight_layout()  # Adjust spacing between plots
        plt.show()

    def save_graph(self, save_dir):
        save_path = save_dir

        year = self.metadata["year"]
        date = self.metadata["date"]
        save_path += f"{date}_{year}.png"

        self.fig.savefig(save_path)
