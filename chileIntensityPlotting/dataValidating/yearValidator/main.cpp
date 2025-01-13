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

bool imgInCorrectYear(std::filesystem::path imgPath, std::string year)
{
    std::ifstream file(imgPath, std::ios::binary);
    if (!file)
    {
        std::print(stderr, "Error opening file: {}\n", imgPath.string());
        return true;
    }

    const long startPosition = 267;
    file.seekg(startPosition, std::ios::beg);
    if (!file)
    {
        std::print(stderr, "Error seeking in file: {}\n", imgPath.string());
        return true;
    }

    char buffer[3];
    file.read(buffer, 3);

    std::uint32_t fileYear = parseBinary(buffer, 3);
    fileYear += 1900; // Year is stored relative to 1900
    std::uint32_t pathYear = std::stoi(year);

    return fileYear == pathYear;
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

void validateNight(std::filesystem::path nightPath, std::string year)
{
    std::vector<std::filesystem::path> toCheck;
    auto entries = std::filesystem::directory_iterator(nightPath);
    for (auto&& entry : entries)
    {
        if (entry.is_directory())
        {
            continue;
        }
        for (const std::string& pattern : IMG_PATTERNS)
        {
            std::string pattern_text = pattern;
            auto regexpr = std::regex(pattern_text);
            std::basic_string filename = entry.path().filename().string();
            if (std::regex_match(filename.begin(), filename.end(), regexpr))
            {
                toCheck.push_back(entry.path());
            }
        }
    }

    for (std::filesystem::path& path : toCheck)
    {
        if (!imgInCorrectYear(path, year))
        {
            std::print("Previous year's data found in {} at image {}.\n", nightPath.string(), path.string());
            break;
        }
    }
}

void validateMonth(std::filesystem::path monthPath, std::string year)
{
    // NOTE: The following assumes that progam is called above year directory, and that there are no
    // month stems in the filepath besides the one that's relevant
    std::string monthStem;
    for (const std::string& month : MONTH_HEADERS)
    {
        if (monthPath.string().find(month) != std::string::npos)
        {
            monthStem = month;
            break;
        }
    }

    std::string pattern_text = monthStem + "[0-3][0-9]-[0-3][0-9]";
    auto regexpr = std::regex(pattern_text);

    std::vector<std::filesystem::path> rawImgPaths = std::vector<std::filesystem::path>();
    auto entries = std::filesystem::directory_iterator(monthPath);
    for (auto&& entry : entries)
    {
        if (!entry.is_directory())
        {
            continue;
        }
        std::basic_string testPath = entry.path().string();
        if (std::regex_search(testPath.begin(), testPath.end(), regexpr))
        {
            rawImgPaths.push_back(entry.path());
        }
    }
    for (auto& path : rawImgPaths)
    {
        validateNight(path, year);
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
        std::print(" --- Validating Year: {} --- \n", year);
        validateYear(year);
        std::print("Year {} done.\n\n", year);
    }
}
