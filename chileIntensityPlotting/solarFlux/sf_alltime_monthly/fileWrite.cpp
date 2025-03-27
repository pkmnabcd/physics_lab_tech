#include "fileWrite.hpp"

#include "OneYear.hpp"

#include <cstdint>
#include <filesystem>
#include <format>
#include <fstream>
#include <string>
#include <vector>

std::uint8_t sfMonthInOHIndex(OneYear year, std::uint8_t month)
{
    std::vector<std::uint8_t> collapsedOHMonths = year.getCollapsedOHMonths();
    for (std::uint8_t i = 0; i < collapsedOHMonths.size(); i++)
    {
        std::uint8_t ohMonth = collapsedOHMonths[i];
        if (ohMonth == month)
        {
            return i;
        }
    }
    return 255;
}

bool writeAveragesToCSV(std::vector<OneYear>& years, std::string outputPathStr)
{
    auto outPath = std::filesystem::path(outputPathStr);
    std::ofstream file = std::ofstream(outPath);
    if (file.is_open())
    {
        for (OneYear& year : years)
        {
            std::vector<std::uint8_t> ohMonths = year.getgetCollapsedOHMonths();
            std::vector<std::uint8_t> sfMonths = year.getgetCollapsedSfMonths();

            std::vector<double> ohAvgs = year.getOHAverage();
            std::vector<double> sfAvgs = year.getSfAverage();
            std::vector<double> ohStdDevs = year.getOHStdDev();
            std::vector<double> sfStdDevs = year.getSfStdDev();

            for (std::uint8_t monthIndex = 0; monthIndex < sfMonths.size(); monthIndex++)
            {
                std::uint8_t ohIndex = sfMonthInOHIndex(year, month);
                if (ohIndex != 255)
                {
                }
                else
                {
                }
            }
            // TODO: Fix this whole file

            file << std::format("{},{},{},{},{}\n", year.getYear(), year.getOHAverage(), year.getSolarAverage(), year.getOHStdDev(), year.getSolarStdDev());
        }
        file.close();
    }
    else
    {
        return false;
    }
    return true;
}
