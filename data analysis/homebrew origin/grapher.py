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
                 graph2: SingleGraph, graph3: SingleGraph, metadata: dict):
        pass

    def generate_graph(self):
        pass

    def save_graph(self, save_dir):
        pass
