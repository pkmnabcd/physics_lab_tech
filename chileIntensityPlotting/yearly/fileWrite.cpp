#include "fileWrite.hpp"

#include "OneDay.hpp"
#include "strTool.hpp"

#include <filesystem>
#include <format>
#include <fstream>
#include <string>
#include <vector>

unsigned int getMonthInt(OneDay day)
{
    std::string month = day.getMonth();
    // TODO: fix this
    if (month == "Jan")
    {
        return 1;
    }
    if (month == "Feb")
    {
        return 2;
    }
    if (month == "Mar")
    {
        return 3;
    }
    if (month == "Apr")
    {
        return 4;
    }
    if (month == "May")
    {
        return 5;
    }
    if (month == "Jun")
    {
        return 6;
    }
    if (month == "Jul")
    {
        return 7;
    }
    if (month == "Aug")
    {
        return 8;
    }
    if (month == "Sep")
    {
        return 9;
    }
    if (month == "Oct")
    {
        return 10;
    }
    if (month == "Nov")
    {
        return 11;
    }
    if (month == "Dec")
    {
        return 12;
    }
    return 0;
}

bool writeAveragesToCSV(std::string yearPath, std::vector<OneDay>& yearAverages, std::string& outputPathStr)
{
    auto outPath = std::filesystem::path(yearPath);
    outPath /= (getYearFromPath(yearPath) + "dailyAverages.csv");
    outputPathStr = outPath.string();
    std::ofstream file = std::ofstream(outPath);
    if (file.is_open())
    {
        for (OneDay& day : yearAverages)
        {
            unsigned int monthInt = getMonthInt(day);
            file << std::format("{},{},{},{}\n", day.getDayOfYear(), monthInt, day.getAverage(), day.getStdDev());
        }
        file.close();
    }
    else
    {
        return false;
    }
    return true;
}
