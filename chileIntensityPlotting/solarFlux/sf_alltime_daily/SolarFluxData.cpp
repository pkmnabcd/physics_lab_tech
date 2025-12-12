#include "SolarFluxData.hpp"

#include <cassert>
#include <cmath>
#include <cstdint>
#include <string>
#include <vector>

SolarFluxData::SolarFluxData(std::vector<std::uint16_t> years, std::vector<std::uint8_t> months, std::vector<std::uint16_t> days, std::vector<double> dailyAverages) :
    m_years(years),
    m_months(months),
    m_days(days),
    m_dailyAverages(dailyAverages)
{
}
