#include "OneDay.hpp"
#include "parsing.hpp"
#include "strTool.hpp"

#include <filesystem>
#include <print>
#include <regex>
#include <string>
#include <vector>

const std::vector<std::string> MONTH_HEADERS = {
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
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

void testDarkIntensities(OneDay day, std::string year)
{
    std::vector<double> darkIntensities = day.getDarkIntensity();
    unsigned int doy = day.getDayOfYear();
    for (double dark : darkIntensities)
    {
        if (dark < 0 || dark > 50000)
        {
            std::print("WARNING: Strange Dark Intensity detected in year {} at day {}.\n", year, doy);
            break;
        }
    }
}

void validateMonth(std::filesystem::path monthPath, std::string year)
{
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
        OneDay oneDay = parseOneDay(path);
        testDarkIntensities(oneDay, year);
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
