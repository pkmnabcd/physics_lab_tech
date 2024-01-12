import pandas as pd


# This function sets the path to import the .csv file
def import_path_making(year):
    initial_path = 'C://Users//42gde//PycharmProjects//physics_lab_tech_job//interference and wave correlation//in_csv//'
    path = initial_path + "ChileMTM_" + year + "_weather_and_processing.csv"

    return path


# Reads in the .csv file according to the path
def import_csv_to_df(path):
    infile = pd.read_csv(path)

    # Remove irrelevant columns
    infile_minus_notes = infile[["date", "interference?", "possible wave?"]]
    # Test for and remove extra rows
    row_count = len(infile_minus_notes)
    df = pd.DataFrame({"date": [], "interference?": [], "possible wave?": []})
    for i in range(row_count):
        # Test if row is empty, add non-empty ones to df
        if not pd.isnull((infile_minus_notes.iloc[i, 0])):
            df = pd.concat([df, infile_minus_notes.iloc[[i]]], ignore_index=True)
    return df
