#include "mean.hpp"

#include "parsing.hpp"
#include "strTool.hpp"

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
    if (dayNumbers[0] == 1)
    {
        auto numOne = dayNumbers[0];
        dayNumbers.erase(0);
        dayNumbers.push_back(numOne);

        auto pathOne = paths[0];
        paths.erase(0);
        paths.push_back(pathOne);
    }
}

void sortOHPaths(std::vector<std::filesystem::path>& paths)
{
    auto filenames = std::vector<std::string>();
    std::cout << paths.size() << std::endl;
    for (auto& path : paths) // For future improvement for simplicity, a path has the method filename() , so you can just use that.
    {
        std::string pathStr = path.string();
        auto filenamePosition = pathStr.find_last_of("/") + 1;
        std::string filename = pathStr.substr(filenamePosition);
        filenames.push_back(filename);
        std::cout << filename << std::endl;
    }
    auto dayNumbers = std::vector<unsigned int>();
    for (auto& filename : filenames)
    {
        auto doyStartPosition = filename.find('y') + 1;
        auto doyEndPosition = filename.find('.') - 1;
        auto positionDelta = doyEndPosition - doyStartPosition;
        std::string doy = "";
        for (unsigned int i = 0; i <= positionDelta; i++)
        {
            doy += filename[doyStartPosition + i];
        }
        dayNumbers.push_back(std::stoi(doy));
    }
    doSelectionSort(paths, dayNumbers);
}

// TODO: write this function
std::vector<std::vector<double>> getMonthlyAverages(std::filesystem::path monthPath)
{
    auto dataPath = monthPath / "processed";
    std::cout << "Finding paths in month path " << dataPath << std::endl;

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
    std::cout << "Out of sort" << std::endl;

    auto output = std::vector<std::vector<double>>();
    for (auto& path : OHPaths)
    {
        std::cout << path.string() << std::endl;
        // TODO: write the parser function in parsing.cpp
        OneDay oneDay = parseOneDay(path);
        // Get the average for the day
        // Add the doy and average to output
    }

    std::cout << "Made it through getMontlyAverages" << std::endl;
    return { { 0.0 } }; // This is intentionally bad so it crashes when the 2nd array is accessed
}

std::vector<std::vector<double>> getYearlyAverages(std::string yearPathStr)
{
    auto yearPath = std::filesystem::path(yearPathStr);
    std::cout << "Path from yearPath: " << yearPath << std::endl;
    std::string year = getYearFromPath(yearPath.string());
    std::cout << "Output year: " << year << std::endl;

    // Temp for demo purposes
    auto entries = std::filesystem::directory_iterator(yearPath);
    for (auto&& entry : entries)
    {
        std::cout << entry << std::endl;
    }

    // Temp print month paths
    std::vector<std::filesystem::path> monthPaths = getMonthPaths(yearPath);
    for (auto path : monthPaths)
    {
        std::cout << path.string() << std::endl;
    }

    std::vector<std::vector<double>> yearlyAverages = { {}, {} };
    for (auto path : monthPaths)
    {
        std::vector<std::vector<double>> monthlyAverages = getMonthlyAverages(path);
        // Test output and make sure there are only two columns
        // Also test to make sure that both arrays are same length

        std::vector<double> time = monthlyAverages[0];
        std::vector<double> temps = monthlyAverages[1];
        for (unsigned int i = 0; i < time.size(); i++)
        {
            // TODO: Make sure the month arrays are ordered
            yearlyAverages[0].push_back(time[i]);
            yearlyAverages[1].push_back(temps[i]);
        }
    }

    //
    // Call function to get all the averages from this month
    //
    // Combine the individual month's averages into one array
    //
    // The array will just be an array of an array of doubles. One array being the day of year (casted to double) and the other array being the average temps
    //
    // Return this

    std::vector<std::vector<double>> return_temp = { { 0.0 } };
    return return_temp;
}
