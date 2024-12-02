#include "OneDay.hpp"
#include "fileWrite.hpp"
#include "mean.hpp"

#include <iostream>
#include <string>
#include <vector>

int main(int argc, char** argv)
{
    if (argc == 1)
    {
        std::cout << "Usage: ..../YearlyGrapher YEAR_FOLDER_PATH" << std::endl;
        return 0;
    }
    std::string year_folder = argv[1];
    std::vector<OneDay> yearAverages = getYearlyAverages(year_folder);

    if (writeAveragesToCSV(year_folder, yearAverages))
    {
        std::cout << "Averages file written.\n";
    }
    else
    {
        std::cout << "Averages file NOT written.\n";
    }

    return 0;
}
