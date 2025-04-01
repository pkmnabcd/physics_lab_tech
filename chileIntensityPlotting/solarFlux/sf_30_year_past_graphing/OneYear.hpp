#pragma once

#include <cstdint>
#include <string>
#include <vector>

class OneYear
{
  public:
    OneYear(std::string year, std::vector<double> dailyOHAvg, std::vector<double> dailySfAvg, std::vector<std::uint8_t> OHMonths, std::vector<std::uint8_t> sfMonths);

    std::string getYear() { return m_year; }
    std::vector<double> getDailyOHAvg() { return m_dailyOHAvg; }
    std::vector<double> getDailySfAvg() { return m_dailySfAvg; }
    std::vector<std::uint8_t> getCollapsedOHMonths() { return m_collapsedOHMonths; }
    std::vector<std::uint8_t> getCollapsedSfMonths() { return m_collapsedSfMonths; }
    std::vector<std::uint8_t> getOHMonths() { return m_OHMonths; }
    std::vector<std::uint8_t> getSfMonths() { return m_sfMonths; }

    std::vector<double> getOHAverage() { return m_OHMonthlyAverages; }
    std::vector<double> getOHStdDev() { return m_OHMonthlyStdDevs; }
    std::vector<double> getSfAverage() { return m_sfMonthlyAverages; }
    std::vector<double> getSfStdDev() { return m_sfMonthlyStdDevs; }

  private:
    const std::string m_year;
    std::vector<double> m_dailyOHAvg;
    std::vector<double> m_dailySfAvg;
    std::vector<std::uint8_t> m_OHMonths;
    std::vector<std::uint8_t> m_sfMonths;

    std::vector<std::uint8_t> m_collapsedOHMonths;
    std::vector<std::uint8_t> m_collapsedSfMonths;
    std::vector<double> m_OHMonthlyAverages;
    std::vector<double> m_sfMonthlyAverages;
    std::vector<double> m_OHMonthlyStdDevs;
    std::vector<double> m_sfMonthlyStdDevs;

    void computeSaveOHAverage();
    void computeSaveSfAverage();
    void computeSaveOHStdDev();
    void computeSaveSfStdDev();
    void collapseOHMonths();
    void collapseSfMonths();
};
