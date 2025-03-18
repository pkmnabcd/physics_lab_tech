#pragma once

#include <cstdint>
#include <string>
#include <vector>

class OneYear
{
  public:
    OneYear(std::string year, std::vector<double> dailyOHAvg, std::vector<double> dailySolarAvg, std::vector<std::uint8_t> months);

    std::string getYear() { return m_year; }
    std::vector<double> getDailyOHAvg() { return m_dailyOHAvg; }
    std::vector<double> getDailySolarAvg() { return m_dailySolarAvg; }
    std::vector<std::uint8_t> getMonths() { return m_months; }

    std::vector<double> getOHAverage() { return m_OHMonthlyAverages; }
    std::vector<double> getOHStdDev() { return m_OHMonthlyStdDevs; }
    std::vector<double> getSolarAverage() { return m_SolarMonthlyAverages; }
    std::vector<double> getSolarStdDev() { return m_SolarMonthlyStdDevs; }

  private:
    const std::string m_year;
    std::vector<double> m_dailyOHAvg;
    std::vector<double> m_dailySolarAvg;
    std::vector<std::uint8_t> m_months;

    std::vector<double> m_OHMonthlyAverages;
    std::vector<double> m_OHMonthlyStdDevs;
    std::vector<double> m_SolarMonthlyAverages;
    std::vector<double> m_SolarMonthlyStdDevs;

    void computeSaveAverage();
    void computeSaveStdDev();
};
