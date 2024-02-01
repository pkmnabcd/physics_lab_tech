from grapher import grapher
import subfolder_generation as sub


def main():
    year = "2019"
    year_filepath = "E://" + year + "//"
    # "F://MERRA-2_Data//" + year + "//"

    lat_subfolder = sub.lat_subfolder(0, is_plus=False)
    lon_subfolder = sub.lon_subfolder(0)
    davis_subfolder = "Davis"

    current_subfolder = lon_subfolder

    grapher(year_filepath, current_subfolder, graph_temp=True, graph_winds=False, graph_year=False, graph_months=False, altitude_level=1,
            day_emphasis_bar=255, smoothing=False, residual_analysis_graph=False, polynomial_best_fit=3,
            do_all_altitudes=False, do_every_other_altitude=False)


main()
