#include "parsing.hpp"

#include "SolarFluxData.hpp"

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

SolarFluxData parseSolarFlux()
{
    // NOTE: Get solar flux lines
    auto solarPath = std::filesystem::path("solarFlux.txt");
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
    std::vector<std::uint16_t> years;
    std::vector<std::uint8_t> months;
    std::vector<std::uint16_t> days;
    std::vector<double> dailySfAverages;

    for (std::string& currentLine : solarLines)
    {
        std::string yearStr = currentLine.substr(0, 4);
        years.push_back(static_cast<std::uint16_t>(std::stoi(yearStr)));

        std::string monthStr = currentLine.substr(5, 2);
        months.push_back(static_cast<std::uint8_t>(std::stoi(monthStr)));

        std::string dayStr = currentLine.substr(8, 2);
        days.push_back(static_cast<std::uint16_t>(std::stoi(dayStr)));

        std::string solarFluxObserved = currentLine.substr(139, 9);
        dailySfAverages.push_back(std::stod(solarFluxObserved));
    }
    return SolarFluxData(years, months, days, dailySfAverages);
}
