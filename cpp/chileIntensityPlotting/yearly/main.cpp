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
    std::vector<std::vector<double>> yearAverages = getYearlyAverages(year_folder);
    std::cout << "Made it to the end\n";

    for (unsigned int i = 0; i < yearAverages[0].size(); i++)
    {
        std::cout << yearAverages[0][i] << " : " << yearAverages[1][i] << std::endl;
    }

    return 0;
}
