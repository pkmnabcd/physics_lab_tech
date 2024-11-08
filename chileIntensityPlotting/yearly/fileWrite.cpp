#include "fileWrite.hpp"

#include "strTool.hpp"

#include <filesystem>
#include <fstream>
#include <string>
#include <vector>

bool writeAveragesToCSV(std::string yearPath, std::vector<std::vector<double>>& yearAverages)
{
    auto outPath = std::filesystem::path(yearPath);
    outPath / (getYearFromPath(yearPath) + "dailyAverages");
    std::ofstream file = std::ofstream(outPath);
    // file.open(path);
    if (file.is_open())
    {
        for (unsigned int i = 0; i < yearAverages[0].size(); i++)
        {
            file << static_cast<int>(yearAverages[0][i]) << "," << yearAverages[1][i] << "\n";
        }
        file.close();
    }
    else
    {
        return false;
    }
    return true;
}
