#include "fileWrite.hpp"

#include "OneDay.hpp"
#include "strTool.hpp"

#include <filesystem>
#include <format>
#include <fstream>
#include <string>
#include <vector>

bool writeAveragesToCSV(std::string yearPath, std::vector<OneDay>& yearAverages)
{
    auto outPath = std::filesystem::path(yearPath);
    outPath /= (getYearFromPath(yearPath) + "dailyAverages.csv");
    std::ofstream file = std::ofstream(outPath);
    if (file.is_open())
    {
        for (OneDay& day : yearAverages)
        {
            file << std::format("{},{},{}\n", day.getDayOfYear(), day.getAverage(), day.getStdDev());
        }
        file.close();
    }
    else
    {
        return false;
    }
    return true;
}
