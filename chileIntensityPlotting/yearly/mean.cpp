#include "mean.hpp"

#include "parsing.hpp"
#include "strTool.hpp"

#include <cmath>
#include <filesystem>
#include <optional>
#include <print>
#include <regex>
#include <string>
#include <vector>

std::uint8_t getHourLength(OneDay day, std::string yearStr)
{
    int year = std::stoi(yearStr);
    if (year < 2011)
    {
        return 10;
    }
    else if (year == 2011)
    {
        unsigned int doy = day.getDayOfYear();
        if (doy < 319 && doy != 1)
        {
            return 10;
        }
        else
        {
            return 33;
        }
    }
    else if (year < 2023)
    {
        return 33;
    }
    else if (year == 2023)
    {
        unsigned int doy = day.getDayOfYear();
        if (doy < 281 && doy != 1)
        {
            return 33;
        }
        else
        {
            return 10;
        }
    }
    else
    {
        return 10;
    }
}

std::vector<std::filesystem::path> getMonthPaths(std::filesystem::path yearPath)
{
    std::string year = getYearFromPath(yearPath.string());

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
    for (auto& path : paths)
    {
        filenames.push_back(path.filename().string());
    }
    auto dayNumbers = std::vector<unsigned int>();
    for (auto& filename : filenames)
    {
        dayNumbers.push_back(parseDoyFromFilename(filename));
    }
    doSelectionSort(paths, dayNumbers);
}

std::optional<double> calculateAverage(OneDay dayData, bool doingTest, std::string year)
{
    double total = 0;
    std::vector<double> temperature = dayData.getOHTemp();
    // NOTE: Either 10 or 33 depending on the date
    std::uint8_t hourLen = getHourLength(dayData, year);
    if (temperature.size() < hourLen && !doingTest)
    {
        std::print("Skipping day {} because it's too short.\n", dayData.getDayOfYear());
        return {};
    }
    else
    {
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
        return { average };
    }
}

double calculateStdDev(OneDay dayData)
{
    double mean = dayData.getAverage();
    std::vector<double> OHTemp = dayData.getOHTemp();
    unsigned int numberOfVals = static_cast<unsigned int>(OHTemp.size());
    double summation = 0;

    for (double val : OHTemp)
    {
        if (std::isnan(val))
        {
            numberOfVals--;
        }
        else
        {
            summation += pow((val - mean), 2);
        }
    }
    double stdDev = sqrt(summation / (numberOfVals - 1));
    return stdDev;
}

std::vector<OneDay> getMonthlyAverages(std::filesystem::path monthPath, std::string year)
{
    auto dataPath = monthPath / "processed";

    std::string pattern_text = "OH_Andover_ALO[0-9][0-9]day[0-9]{1,3}e.dat";
    auto regexpr = std::regex(pattern_text);

    std::vector<std::filesystem::path> OHPaths = std::vector<std::filesystem::path>();
    auto entries = std::filesystem::directory_iterator(dataPath);
    for (auto&& entry : entries)
    {
        if (entry.is_directory())
        {
            continue;
        }
        std::basic_string filename = entry.path().filename().string();
        if (std::regex_match(filename.begin(), filename.end(), regexpr))
        {
            OHPaths.push_back(entry.path());
        }
    }
    sortOHPaths(OHPaths);

    auto output = std::vector<OneDay>();
    for (auto& path : OHPaths)
    {
        OneDay oneDay = parseOneDay(path);
        std::optional<double> avg = calculateAverage(oneDay, false, year);
        if (avg.has_value())
        {
            oneDay.setAverage(avg.value());
            oneDay.setStdDev(calculateStdDev(oneDay));

            // Getting rid of vectors we don't need anymore
            oneDay.setTime(std::vector<double>());
            oneDay.setOHTemp(std::vector<double>());

            output.push_back(oneDay);
        }
        else
        {
            continue;
        }
    }

    return output;
}

std::vector<OneDay> getYearlyAverages(std::string yearPathStr)
{
    auto yearPath = std::filesystem::path(yearPathStr);
    std::string year = getYearFromPath(yearPath.string());

    std::vector<std::filesystem::path> monthPaths = getMonthPaths(yearPath);
    std::vector<OneDay> yearlyAverages = {};
    for (auto path : monthPaths)
    {
        std::vector<OneDay> monthlyAverages = getMonthlyAverages(path, year);

        for (OneDay& day : monthlyAverages)
        {
            yearlyAverages.push_back(day);
        }
    }
    return yearlyAverages;
}
