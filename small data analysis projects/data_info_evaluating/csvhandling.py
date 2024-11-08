import pandas as pd
from misc import month_converting
from os.path import exists


# This function sets the path to import the .csv file
def import_path_making(month_int, year):
    initial_path = 'C://Users//42gde//PycharmProjects//physics_lab_tech_job//data_info_evaluating//ChileMTM_info//' + year + '//'
    month = month_converting(month_int)
    path = initial_path + year + '_' + month + '_ChileMTM_info.csv'

    return path


# Reads in the .csv file according to the path
def import_csv_to_df(path):
    infile = pd.read_csv(path)

    # Remove irrelevant columns
    infile_minus_notes = infile[['date ', 'star removed (sr)', 'flat fielded (ff)', 'calibrated, unwarped (caun)']]
    # Test for and remove extra rows
    row_count = len(infile_minus_notes)
    df = pd.DataFrame({'date ': [], 'star removed (sr)': [], 'flat fielded (ff)': [], 'calibrated, unwarped (caun)': []})
    for i in range(row_count):
        # Test if row is empty, add non-empty ones to df
        if not pd.isnull((infile_minus_notes.iloc[i, 0])):
            df = pd.concat([df, infile_minus_notes.iloc[[i]]], ignore_index=True)
    return df


# Sets the path for the output .csv file
def export_path_base_making():
    path = 'C://Users//42gde//PycharmProjects//physics_lab_tech_job//data_info_evaluating//output_csv//data_info_out'
    return path


# Makes output .csv file
def export_csv(out_array):
    base_path = export_path_base_making()
    in_path_plus_csv = base_path + '.csv'
    path = in_path_plus_csv

    if not exists(in_path_plus_csv):
        out_array.to_csv(path, index=False)
        print('File Outputted')
    else:
        count = 0
        while exists(path):
            count += 1
            path = base_path + '(' + str(count) + ').csv'
            if not exists(path):
                out_array.to_csv(path, index=False)
                print('File Outputted')
                break
