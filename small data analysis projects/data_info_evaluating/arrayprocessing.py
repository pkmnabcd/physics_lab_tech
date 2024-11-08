import pandas as pd
import matplotlib.pyplot as plt
from misc import month_converting


# This function makes a new column that includes the average of column in percentage form
def monthly_averages(in_array, month_index):
    total_number = len(in_array)  # This is how many rows there are
    out_array = pd.DataFrame({'date ': month_converting(month_index) + '_avg', 'star removed (sr)': [0], 'flat fielded (ff)': [0], 'calibrated, unwarped (caun)': [0]})

    for column in in_array.columns[1:]:  # Selects each column of the input array
        col_total = 0

        for i in in_array[column]:  # Selects each row in the column
            col_total += i
        col_average = col_total / total_number * 100
        out_array.loc[0, column] = col_average
    return out_array


# This function makes barplots of the averages across the year
def avg_plot(df, year):
    df.plot.bar(xlabel='Month', ylabel="Percentage of Data Processed", rot=0, figsize=(12, 8), title=year + " monthly a\
verages")
    plt.show()


# This function takes the avg array and raw data array for each month and makes a one-line array with new columns
def output_processing(raw_data, avg_data, month, year):
    # Make the date value
    date = month_converting(month) + '_' + year

    day_count = len(raw_data)

    # Get the sum of each category
    sr_sum = sum(raw_data['star removed (sr)'])
    ff_sum = sum(raw_data['flat fielded (ff)'])
    caun_sum = sum(raw_data['calibrated, unwarped (caun)'])
    # Get the avg of each category
    sr_avg = avg_data['star removed (sr)']
    ff_avg = avg_data['flat fielded (ff)']
    caun_avg = avg_data['calibrated, unwarped (caun)']

    # Combine into output array
    out_dict = {'date ': date, 'sr count': sr_sum, 'sr percent': sr_avg, 'ff count': ff_sum, 'ff percent': ff_avg,
                'caun count': caun_sum, 'caun percent': caun_avg}
    out_array = pd.DataFrame(out_dict)
    return out_array
