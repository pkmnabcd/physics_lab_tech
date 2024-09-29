#include "mean.hpp"

#include "strTool.hpp"

#include <filesystem>
#include <iostream>
#include <string>
#include <vector>

double getYearlyAverage(std::string yearPathStr)
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

    return 0.0;
}

// std::vector<std::filesystem::path> getMonthPaths(std::string yearPathStr,
