#include "fileWrite.hpp"

#include "OneDay.hpp"
#include "strTool.hpp"

#include <filesystem>
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
            file << day.getDayOfYear() << "," << day.getAverage() << "\n";
        }
        file.close();
    }
    else
    {
        return false;
    }
    return true;
}
