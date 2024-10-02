#include "mean.hpp"

#include "strTool.hpp"

#include <filesystem>
#include <format>
#include <iostream>
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



std::vector<std::vector<double>> getYearlyAverages(std::string yearPathStr)
{
    auto yearPath = std::filesystem::path(yearPathStr);
    std::cout << "Path from yearPath: " << yearPath << std::endl;
    std::string year = getYearFromPath(yearPath.string());
    std::cout << "Output year: " << year << std::endl;

    auto entries = std::filesystem::directory_iterator(yearPath);
    for (auto&& entry : entries)
    {
        std::cout << entry << std::endl;
    }
    // Get month paths
    std::vector<std::filesystem::path> monthPaths = getMonthPaths(yearPath);
    for (auto path : monthPaths)
    {
        std::cout << path.string() << std::endl;
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
