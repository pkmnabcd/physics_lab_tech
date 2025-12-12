#include "fileWrite.hpp"

#include "SolarFluxData.hpp"

#include <cassert>
#include <cstdint>
#include <filesystem>
#include <format>
#include <fstream>
#include <string>
#include <vector>

bool writeAveragesToCSV(SolarFluxData& sfData, std::string outputPathStr)
{
    const std::vector<std::uint16_t> years = sfData.getYears();
    const std::vector<std::uint8_t> months = sfData.getMonths();
    const std::vector<std::uint16_t> days = sfData.getDays();
    const std::vector<double> sfAverages = sfData.getAverages();
    assert(years.size() == months.size() && "Each data point have a year, month, day, and average.");
    assert(years.size() == days.size() && "Each data point have a year, month, day, and average.");
    assert(years.size() == sfAverages.size() && "Each data point have a year, month, day, and average.");

    auto outPath = std::filesystem::path(outputPathStr);
    std::ofstream file = std::ofstream(outPath);
    if (file.is_open())
    {
        for (std::uint32_t i = 0; i < years.size(); i++)
        {
            file << std::format("{},{},{},{}\n", years[i], months[i], days[i], sfAverages[i]);
        }
        file.close();
        return true;
    }
    else
    {
        return false;
    }
}
