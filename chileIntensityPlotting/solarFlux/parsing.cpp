#include "parsing.hpp"

#include "OneYear.hpp"

#include <cassert>
#include <cmath>
#include <cstdint>
#include <filesystem>
#include <format>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

std::vector<std::string> split(std::string input, std::uint8_t ch)
{
    std::vector<std::string> output;
    if (!input.contains(ch))
    {
        output.push_back(input);
        return output;
    }

    std::string beforeCh;
    for (std::uint16_t i = 0; i < input.size(); i++)
    {
        if (input[i] == ch)
        {
            // NOTE: This implementation isn't expecting empty values
            if (beforeCh != "")
            {
                output.push_back(beforeCh);
                beforeCh = "";
            }
        }
        else
        {
            beforeCh.push_back(input[i]);
        }
    }
    if (beforeCh != "")
    {
        output.push_back(beforeCh);
    }
    return output;
}

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

    // NOTE: Parsing the OH lines
    std::vector<double> dailyOHAverages;
    for (std::string& line : OHLines)
    {
        std::vector<std::string> splitLine = split(line, ',');
        assert(splitLine.size() == 3 && "YEARdailyAverages.csv must have 3 columns");
        dailyOHAverages.push_back(std::stod(splitLine[1]));
    }

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
    file.close();

    // NOTE: Parsing the solar lines
    std::vector<double> dailySolarAverages;
    for (std::string& line : solarLines)
    {
        std::vector<std::string> splitLine = split(line, ',');
        assert(splitLine.size() == 3 && "noaa_radio_flux.csv must have 3 columns");
        std::uint16_t currentYearInt = std::stoi(year);
        std::uint16_t lineYear = std::stoi(splitLine[0].substr(0, 4));
        if (currentYearInt > lineYear)
        {
            continue;
        }
        else if (currentYearInt == lineYear)
        {
            dailySolarAverages.push_back(std::stod(splitLine[1]));
        }
        else
        {
            break; // Assumes time goes from least to greatest
        }
    }

    return OneYear(year, dailyOHAverages, dailySolarAverages);
}
