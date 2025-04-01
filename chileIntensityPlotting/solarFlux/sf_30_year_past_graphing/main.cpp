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
    for (std::uint16_t yearInt = 1979; yearInt < 2010; yearInt++)
    {
        std::string year = std::to_string(yearInt);
        std::print(" --- Getting the Monthly Average Solar Flux for Year: {} --- \n", year);
        yearlyMeans.push_back(parseOneYear(year));
        std::print("Year {} done.\n\n", year);
    }

    std::string outputPathStr = "30_years_past_sf_month_averages.csv";
    if (writeAveragesToCSV(yearlyMeans, outputPathStr))
    {
        std::cout << "Averages file written to " << outputPathStr << " .\n";
#ifdef _WIN32
        std::string command = "python solar30YearsPastMonthlyGrapher.py ";
#else
        std::string command = "python3 solar30YearsPastMonthlyGrapher.py ";
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
