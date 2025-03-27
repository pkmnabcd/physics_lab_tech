#include "OneYear.hpp"
#include "fileWrite.hpp"
#include "parsing.hpp"

#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <print>
#include <string>
#include <vector>

int main()
{
    std::vector<OneYear> yearlyMeans;
    for (std::uint16_t yearInt = 2009; yearInt < 2025; yearInt++)
    {
        std::string year = std::to_string(yearInt);
        std::print(" --- Getting the Yearly Average OH Temp and Solar Flux for Year: {} --- \n", year);
        yearlyMeans.push_back(parseOneYear(year));
        std::print("Year {} done.\n\n", year);
    }

    std::string outputPathStr = "all_time_oh_sf_year_averages.csv";
    if (writeAveragesToCSV(yearlyMeans, outputPathStr))
    {
        std::cout << "Averages file written to " << outputPathStr << " .\n";
#ifdef _WIN32
        std::string command = "python solarGrapher.py ";
#else
        std::string command = "python3 solarGrapher.py ";
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
