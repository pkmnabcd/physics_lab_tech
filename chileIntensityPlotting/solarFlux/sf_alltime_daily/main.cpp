#include "SolarFluxData.hpp"
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
    std::print(" --- Getting the Daliy Average Solar Flux ---\n");
    SolarFluxData sfData = parseSolarFlux();
    std::print("Done!\n\n");

    std::string outputPathStr = "all_time_sf_daily_averages.csv";
    if (writeAveragesToCSV(sfData, outputPathStr))
    {
        std::cout << "Averages file written to " << outputPathStr << " .\n";
#ifdef _WIN32
        std::string command = "python solarDaliyGrapher.py ";
#else
        std::string command = "python3 solarDailyGrapher.py ";
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
