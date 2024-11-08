#include "mean.hpp"

#include "parsing.hpp"
#include "strTool.hpp"

#include <cmath>
#include <filesystem>
#include <format>
#include <iostream>
#include <regex>
#include <string>
#include <vector>

std::vector<std::filesystem::path> getMonthPaths(std::filesystem::path yearPath)
{
    std::string year = getYearFromPath(yearPath.string());
    std::cout << std::format("Finding the months paths for the year {}\n.", year);

    std::vector<std::filesystem::path> monthPaths = {};
    for (std::string month : MONTH_HEADERS)
    {
        std::string monthPathStr = yearPath.string() + "/" + month + year + "/";
        auto monthPath = std::filesystem::path(monthPathStr);
        if (std::filesystem::exists(monthPath))
        {
            monthPaths.push_back(monthPath);
        }
    }
    return monthPaths;
}

void doSelectionSort(std::vector<std::filesystem::path>& paths, std::vector<unsigned int>& dayNumbers)
{
    if (paths.size() == 0 && paths.size() == 0)
    {
        return;
    }
    for (unsigned int i = 0; i < paths.size() - 1; i++)
    {
        unsigned int currentMinIndex = i;
        unsigned int currentMinVal = dayNumbers[i];

        for (unsigned int j = i + 1; j < paths.size(); j++)
        {
            if (dayNumbers[j] < currentMinVal)
            {
                currentMinIndex = j;
                currentMinVal = dayNumbers[j];
            }
        }
        if (currentMinIndex != i)
        {
            dayNumbers[currentMinIndex] = dayNumbers[i];
            dayNumbers[i] = currentMinVal;

            auto tempPath = paths[currentMinIndex];
            paths[currentMinIndex] = paths[i];
            paths[i] = tempPath;
        }
    }
}

void sortOHPaths(std::vector<std::filesystem::path>& paths)
{
    auto filenames = std::vector<std::string>();
    for (auto& path : paths) // For future improvement for simplicity, a path has the method filename() , so you can just use that.
    {
        std::string pathStr = path.string();
        auto filenamePosition = pathStr.find_last_of("/") + 1;
        std::string filename = pathStr.substr(filenamePosition);
        filenames.push_back(filename);
    }
    auto dayNumbers = std::vector<unsigned int>();
    for (auto& filename : filenames)
    {
        dayNumbers.push_back(parseDoyFromFilename(filename));
    }
    doSelectionSort(paths, dayNumbers);
}

double getAverage(OneDay dayData)
{
    double total = 0;
    std::vector<double> temperature = dayData.getOHTemp();
    std::uint16_t nanCount = 0;
    for (auto& val : temperature)
    {
        if (std::isnan(val))
        {
            nanCount++;
            continue;
        }
        total += val;
    }
    double average = total / (temperature.size() - nanCount);
    return average;
}

std::vector<std::vector<double>> getMonthlyAverages(std::filesystem::path monthPath)
{
    auto dataPath = monthPath / "processed";

    std::string pattern_text = "/OH_Andover_ALO[0-9][0-9]day[0-9]{1,3}.dat";
    auto regexpr = std::regex(pattern_text);

    std::vector<std::filesystem::path> OHPaths = std::vector<std::filesystem::path>();
    auto entries = std::filesystem::directory_iterator(dataPath);
    for (auto&& entry : entries)
    {
        if (entry.is_directory())
        {
            continue;
        }
        std::basic_string pathString = entry.path().string();
        if (std::regex_search(pathString.begin(), pathString.end(), regexpr))
        {
            OHPaths.push_back(entry.path());
        }
    }
    sortOHPaths(OHPaths);

    auto output = std::vector<std::vector<double>>(2);
    output[0] = std::vector<double>();
    output[1] = std::vector<double>();
    for (auto& path : OHPaths)
    {
        OneDay oneDay = parseOneDay(path);
        output[0].push_back(static_cast<double>(oneDay.getDayOfYear()));
        output[1].push_back(getAverage(oneDay));
    }

    return output;
}

std::vector<std::vector<double>> getYearlyAverages(std::string yearPathStr)
{
    auto yearPath = std::filesystem::path(yearPathStr);
    std::cout << "Path from yearPath: " << yearPath << std::endl;
    std::string year = getYearFromPath(yearPath.string());

    // Temp print month paths
    std::cout << "--Month Paths--\n";
    std::vector<std::filesystem::path> monthPaths = getMonthPaths(yearPath);
    for (auto path : monthPaths)
    {
        std::cout << path.string() << std::endl;
    }

    std::vector<std::vector<double>> yearlyAverages = { {}, {} };
    for (auto path : monthPaths)
    {
        std::vector<std::vector<double>> monthlyAverages = getMonthlyAverages(path);

        std::vector<double> time = monthlyAverages[0];
        std::vector<double> temps = monthlyAverages[1];
        for (unsigned int i = 0; i < time.size(); i++)
        {
            // TODO: Make sure the month arrays are ordered
            yearlyAverages[0].push_back(time[i]);
            yearlyAverages[1].push_back(temps[i]);
        }
    }

    return yearlyAverages;
}
