#include "files.hpp"
#include "mean.hpp"

#include <iostream>
#include <string>

int main(int argc, char** argv)
{
    if (argc == 1)
    {
        std::cout << "Usage: ..../YearlyGrapher YEAR_FOLDER_PATH" << std::endl;
        return 0;
    }
    std::string year_folder = argv[1];

    double year_avg = getYearlyAverage(year_folder);

    return 0;
}
