#include "OneDay.hpp"
#include "OneYear.hpp"
#include "fileWrite.hpp"
#include "mean.hpp"

#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <print>
#include <string>
#include <vector>

int main()
{
    // TODO: Remove this test code
    OneYear test = OneYear("2009", { 1.3, 4.5 }, { 3, 4.1 });
    // TODO: end test code

    std::vector<OneYear> yearlyMeans;
    for (std::uint16_t yearInt = 2009; yearInt < 2025; yearInt++)
    {
        std::string year = std::to_string(yearInt);
        std::print(" --- Getting the Yearly Average OH Temp and Solar Flux for Year: {} --- \n", year);
        yearlyMeans.push_back(getYearAverages(year));
        std::print("Year {} done.\n\n", year);
    }

    std::string outputPathStr = "";
    // TODO: Change this to something relevant
    std::string year_folder = "temp";
    if (writeAveragesToCSV(year_folder, yearlyMeans, outputPathStr))
    {
        std::cout << "Averages file written to " << outputPathStr << " .\n";
#ifdef _WIN32
        std::string command = "python solarFluxGrapher.py ";
#else
        std::string command = "python3 solarFluxGrapher.py ";
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
