#include "OneDay.hpp"
#include "strTool.hpp"

#include <filesystem>
#include <fstream>
#include <iostream>
#include <print>
#include <regex>
#include <string>
#include <vector>

const std::vector<std::string> MONTH_HEADERS = {
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
};

const std::vector<std::string> NIGHTS = { "01-02", "02-03", "03-04", "04-05", "05-06", "06-07", "07-08", "08-09", "09-10", "10-11", "11-12", "12-13", "13-14", "14-15", "15-16", "16-17", "17-18", "18-19", "19-20", "20-21", "21-22", "22-23", "23-24", "24-25", "25-26", "26-27", "27-28", "28-29", "29-30", "30-31", "28-01", "29-01", "30-01", "31-01" };

const std::vector<std::string> IMG_PATTERNS = {
    "866A_[0-9]{4}.tif",
    "868A_[0-9]{4}.tif",
    "BG_[0-9]{4}.tif",
    "Dark_[0-9]{4}.tif",
    "P12A_[0-9]{4}.tif",
    "P14A_[0-9]{4}.tif"
};

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

void testDayTimes(OneDay day, std::string year)
{
    std::vector<double> times = day.getTime();
    unsigned int doy = day.getDayOfYear();
    double prevTime = -9999999;
    for (double time : times)
    {
        if (time < prevTime)
        {
            std::print("WARNING: Time reversion detected in year {} at day {}.\n", year, doy);
        }
        prevTime = time;
    }
}

void validateMonth(std::filesystem::path monthPath, std::string year)
{
    // TODO: start here in making changes
    auto dataPath = monthPath / "processed";

    std::string pattern_text = "OH_Andover_ALO[0-9][0-9]day[0-9]{1,3}.dat";
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
    for (auto& path : OHPaths)
    {
        // OneDay oneDay = parseOneDay(path);
        // testDayTimes(oneDay, year);
    }
}

void validateYear(std::string year)
{
    auto yearPath = std::filesystem::path(year);

    std::vector<std::filesystem::path> monthPaths = getMonthPaths(yearPath);
    for (auto path : monthPaths)
    {
        validateMonth(path, year);
    }
}

int main()
{
    for (int yearInt = 2009; yearInt < 2025; yearInt++)
    {
        std::string year = std::to_string(yearInt);
        validateYear(year);
    }
}
