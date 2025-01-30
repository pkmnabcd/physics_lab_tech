#include "fileWrite.hpp"

#include "OneYear.hpp"

#include <filesystem>
#include <format>
#include <fstream>
#include <string>
#include <vector>

bool writeAveragesToCSV(std::vector<OneYear>& yearAverages, std::string outputPathStr)
{
    auto outPath = std::filesystem::path(outputPathStr);
    std::ofstream file = std::ofstream(outPath);
    if (file.is_open())
    {
        for (OneYear& year : yearAverages)
        {
            // TODO: Fix this whole file

            // file << std::format("{},{},{}\n", year.getDayOfYear(), year.getAverage(), year.getStdDev());
        }
        file.close();
    }
    else
    {
        return false;
    }
    return true;
}
