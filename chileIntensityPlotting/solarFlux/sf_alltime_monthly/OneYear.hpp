#pragma once

#include <cstdint>
#include <string>
#include <vector>

class OneYear
{
  public:
    OneYear(std::string year, std::vector<double> dailyOHAvg, std::vector<double> dailySfAvg, std::vector<std::uint8_t> ohMonths, std::vector<std::uint8_t> sfMonths);

    std::string getYear() { return m_year; }
    std::vector<double> getDailyOHAvg() { return m_dailyOHAvg; }
    std::vector<double> getDailySfAvg() { return m_dailySfAvg; }
    std::vector<std::uint8_t> getMonths() { return m_months; }
    std::vector<std::uint8_t> getOhMonths() { return m_ohMonths; }
    std::vector<std::uint8_t> getSfMonths() { return m_sfMonths; }

    std::vector<double> getOHAverage() { return m_OHMonthlyAverages; }
    std::vector<double> getOHStdDev() { return m_OHMonthlyStdDevs; }
    std::vector<double> getSfAverage() { return m_sfMonthlyAverages; }
    std::vector<double> getSfStdDev() { return m_sfMonthlyStdDevs; }

  private:
    const std::string m_year;
    std::vector<double> m_dailyOHAvg;
    std::vector<double> m_dailySfAvg;
    std::vector<std::uint8_t> m_ohMonths;
    std::vector<std::uint8_t> m_sfMonths;

    std::vector<std::uint8_t> m_months;
    std::vector<double> m_OHMonthlyAverages;
    std::vector<double> m_sfMonthlyAverages;
    std::vector<double> m_OHMonthlyStdDevs;
    std::vector<double> m_sfMonthlyStdDevs;

    void computeSaveOHAverage();
    void computeSaveSfAverage();
    void computeSaveOHStdDev();
    void computeSaveSfStdDev();
    void computeMonths();
};
