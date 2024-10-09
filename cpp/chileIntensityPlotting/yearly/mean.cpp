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

// TODO: write this function
std::vector<std::vector<double>> getMonthlyAverages(std::filesystem::path monthPath)
{
    auto dataPath = monthPath / "processed";

    auto output = std::vector<std::vector<double>>();
    auto entries = std::filesystem::directory_iterator(dataPath);
    for (auto&& entry : entries)
    {
        std::cout << entry << std::endl;
        // Test to make sure it's the right file
        // Parse the data
        // Get the average for the day
        // Add the doy and average to output
    }

    return { { 0.0 } };  // This is intentionally bad so it crashes when the 2nd array is accessed
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
