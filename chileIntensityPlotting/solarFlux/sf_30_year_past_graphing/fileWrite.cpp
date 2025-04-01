#include "fileWrite.hpp"

#include "OneYear.hpp"

#include <cstdint>
#include <filesystem>
#include <format>
#include <fstream>
#include <string>
#include <vector>

bool writeAveragesToCSV(std::vector<OneYear>& years, std::string outputPathStr)
{
    auto outPath = std::filesystem::path(outputPathStr);
    std::ofstream file = std::ofstream(outPath);
    if (file.is_open())
    {
        for (OneYear& year : years)
        {
            std::vector<std::uint8_t> sfMonths = year.getCollapsedSfMonths();

            std::vector<double> sfAvgs = year.getSfAverage();
            std::vector<double> sfStdDevs = year.getSfStdDev();

            for (std::uint8_t monthIndex = 0; monthIndex < sfMonths.size(); monthIndex++)
            {
                std::uint8_t month = sfMonths[monthIndex];
                file << std::format("{},{},{},{}\n", year.getYear(), month, sfAvgs[monthIndex], sfStdDevs[monthIndex]);
            }
        }
        file.close();
    }
    else
    {
        return false;
    }
    return true;
}
