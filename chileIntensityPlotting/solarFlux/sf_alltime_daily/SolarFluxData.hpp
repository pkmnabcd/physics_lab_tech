#pragma once

#include <cstdint>
#include <vector>

class SolarFluxData
{
  public:
    SolarFluxData(std::vector<std::uint16_t> years, std::vector<std::uint8_t> months, std::vector<std::uint16_t> days, std::vector<double> dailyAvgs);

    std::vector<std::uint16_t> getYears() { return m_years; }
    std::vector<std::uint8_t> getMonths() { return m_months; }
    std::vector<std::uint16_t> getDays() { return m_days; }
    std::vector<double> getAverages() { return m_dailyAverages; }

  private:
    const std::vector<std::uint16_t> m_years;
    const std::vector<std::uint8_t> m_months;
    const std::vector<std::uint16_t> m_days;
    const std::vector<double> m_dailyAverages;
};
