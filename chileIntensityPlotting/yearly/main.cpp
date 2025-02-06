#include "OneDay.hpp"
#include "fileWrite.hpp"
#include "mean.hpp"

#include <cstdlib>
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

    std::string outputPathStr = "";
    if (writeAveragesToCSV(year_folder, yearAverages, outputPathStr))
    {
        std::cout << "Averages file written to " << outputPathStr << " .\n";
#ifdef _WIN32
        std::string command = "python yearGrapher.py ";
#else
        std::string command = "python3 yearGrapher.py ";
#endif
        command += outputPathStr;
        std::cout << "Executing the command: " << command << std::endl;
        std::system(command.c_str());
    }
    else
    {
        std::cout << "Averages file NOT written. Grapher not launched.\n";
    }

    return 0;
}
