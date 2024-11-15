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
    std::cout << "Made it to the end\n";

    for (OneDay& day : yearAverages)
    {
        std::cout << day.getDayOfYear() << " : " << day.getAverage() << std::endl;
    }

    if (writeAveragesToCSV(year_folder, yearAverages))
    {
        std::cout << "Written.\n";
    }
    else
    {
        std::cout << "Not Written.\n";
    }

    return 0;
}
