#include "parsing.hpp"

#include "OneDay.hpp"
#include "OneYear.hpp"
#include "strTool.hpp"

#include <cmath>
#include <filesystem>
#include <format>
#include <fstream>
#include <iostream>
#include <vector>

OneYear parseOneYear(std::string year)
{
    // NOTE: Get year OH data
    auto OHPath = std::filesystem::path(std::format("{}dailyAverages.csv", year));

    std::ifstream file = std::ifstream(OHPath);
    std::vector<std::string> OHLines;
    std::string line;
    while (std::getline(file, line))
    {
        OHLines.push_back(line);
    }
    file.close();

    // NOTE: Get year solar flux data
    auto solarPath = std::filesystem::path("noaa_radio_flux.csv");
    file = std::ifstream(solarPath); // Assumes solar flux in pwd
    std::vector<std::string> solarLines;
    line = "";
    std::string headerLine;
    std::uint8_t lineNumber = 1;
    while (std::getline(file, line))
    {
        if (lineNumber == 1)
        {
            headerLine = line;
        }
        else
        {
            solarLines.push_back(line);
        }
        lineNumber++;
    }

    return OneYear(year, { 0 }, { 0 });
}
