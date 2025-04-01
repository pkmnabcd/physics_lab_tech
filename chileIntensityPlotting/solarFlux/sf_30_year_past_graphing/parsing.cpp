#include "parsing.hpp"

#include "OneYear.hpp"

#include <cassert>
#include <cmath>
#include <cstdint>
#include <filesystem>
#include <format>
#include <fstream>
#include <iostream>
#include <print>
#include <string>
#include <vector>

OneYear parseOneYear(std::string year)
{
    // NOTE: Get year solar flux data
    auto solarPath = std::filesystem::path("solarFlux30YearsPast.txt");
    auto file = std::ifstream(solarPath); // Assumes solar flux in pwd
    if (!file.is_open())
    {
        std::print("WARNING: the file at this path: \"{}\" was not found!\n", solarPath.string());
    }
    std::vector<std::string> solarLines;
    std::string line = "";
    while (std::getline(file, line))
    {
        solarLines.push_back(line);
    }
    file.close();

    // NOTE: Parsing the solar lines
    std::vector<double> dailySolarAverages;
    std::vector<std::uint8_t> sfMonths;
    for (std::string& currentLine : solarLines)
    {
        std::uint16_t currentYearInt = static_cast<std::uint16_t>(std::stoi(year));
        std::string lineYear = currentLine.substr(0, 4);
        std::uint16_t lineYearInt = static_cast<std::uint16_t>(std::stoi(lineYear));
        if (currentYearInt > lineYearInt)
        {
            continue;
        }
        else if (currentYearInt == lineYearInt)
        {
            std::string sfMonth = currentLine.substr(5, 2);
            sfMonths.push_back(static_cast<std::uint8_t>(std::stoi(sfMonth)));

            std::string solarFluxObserved = currentLine.substr(139, 9);
            dailySolarAverages.push_back(std::stod(solarFluxObserved));
        }
        else
        {
            break; // Assumes time goes from least to greatest
        }
    }

    return OneYear(year, dailySolarAverages, sfMonths);
}
