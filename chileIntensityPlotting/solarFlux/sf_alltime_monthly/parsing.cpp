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
    auto OHPath = std::filesystem::path(std::format("{0}/{0}dailyAverages.csv", year));

    std::ifstream file = std::ifstream(OHPath);
    if (!file.is_open())
    {
        std::print("WARNING: the file at this path: \"{}\" was not found!\n", OHPath.string());
    }
    std::vector<std::string> OHLines;
    std::string line;
    while (std::getline(file, line))
    {
        OHLines.push_back(line);
    }
    file.close();

    // NOTE: Parsing the OH lines
    std::vector<double> dailyOHAverages;
    std::vector<std::uint8_t> OHMonths;
    for (std::string& currentLine : OHLines)
    {
        std::vector<std::string> splitLine = split(currentLine, ',');
        assert(splitLine.size() == 4 && "YEARdailyAverages.csv must have 4 columns");
        dailyOHAverages.push_back(std::stod(splitLine[2]));
        OHMonths.push_back(static_cast<std::uint8_t>(std::stoul(splitLine[1])));
    }
    assert(dailyOHAverages.size() == OHMonths.size() && "Month and dailyOHAverages vectors have same size");

    // NOTE: Get year solar flux data
    auto solarPath = std::filesystem::path("solarFlux.txt");
    file = std::ifstream(solarPath); // Assumes solar flux in pwd
    if (!file.is_open())
    {
        std::print("WARNING: the file at this path: \"{}\" was not found!\n", solarPath.string());
    }
    std::vector<std::string> solarLines;
    line = "";
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

    // TODO: remove this later

    std::print("{}\n", year);
    std::print("OH averages: \n");
    for (auto& OHAvg : dailyOHAverages)
    {
        std::print("{} ", OHAvg);
    }
    std::print("SF averages: \n");
    for (auto& sfAvg : dailySolarAverages)
    {
        std::print("{} ", sfAvg);
    }
    std::print("OH months: \n");
    for (auto& month : OHMonths)
    {
        std::print("{} ", month);
    }
    std::print("SF months: \n");
    for (auto& month : sfMonths)
    {
        std::print("{} ", month);
    }
    std::print("\n\n");

    // TODO: End remove

    return OneYear(year, dailyOHAverages, dailySolarAverages, OHMonths, sfMonths);
}
