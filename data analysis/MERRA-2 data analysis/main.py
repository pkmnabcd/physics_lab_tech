from grapher import grapher


def main():
    year = "2019"
    year_filepath = "E://" + year + "//"
    # "F://MERRA-2_Data//" + year + "//"

    subfolders = ["McMurdo", "McMurdo_minus_15#1", "McMurdo_minus_15#2", "McMurdo_minus_15#3", "McMurdo_minus_15#4",
                  "McMurdo_minus_15#5", "McMurdo_minus_15#6", "McMurdo_minus_15#7", "McMurdo_minus_15#8",
                  "McMurdo_minus_15#9", "McMurdo_minus_15#10", "McMurdo_minus_15#11", "McMurdo_minus_15#12",
                  "McMurdo_minus_15#13", "McMurdo_minus_15#14", "McMurdo_minus_15#15", "McMurdo_minus_15#16",
                  "McMurdo_minus_15#17", "McMurdo_minus_15#18", "McMurdo_minus_15#19", "McMurdo_minus_15#20",
                  "McMurdo_minus_15#21", "McMurdo_minus_15#22", "McMurdo_minus_15#23", "Davis"]
    current_subfolder = subfolders[0]  # 0 is McMurdo, McMurdo minus is from index 1 to 23, Davis 24

    grapher(year_filepath, current_subfolder, graph_temp=True, graph_winds=False, graph_year=True, graph_months=False, altitude_level=1,
            day_emphasis_bar=255, smoothing=True, residual_analysis_graph=True, polynomial_best_fit=3,
            do_all_altitudes=True, do_every_other_altitude=False)


main()
