#include "mean.hpp"

#include "strTool.hpp"

#include <filesystem>
#include <iostream>
#include <string>
#include <vector>

std::vector<std::vector<std::vector<double>>> getYearlyAverages(std::string yearPathStr)
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
    //
    // Call function to get all the averages from this month
    //
    // Combine the individual month's averages into one array
    //
    // Return this

    std::vector<std::vector<std::vector<double>>> return_temp = { { { 0.0 } } };
    return return_temp;
}

// std::vector<std::filesystem::path> getMonthPaths(std::string yearPathStr,
