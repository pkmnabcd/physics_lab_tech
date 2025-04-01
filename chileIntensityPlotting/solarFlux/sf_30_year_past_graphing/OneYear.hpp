#pragma once

#include <cstdint>
#include <string>
#include <vector>

class OneYear
{
  public:
    OneYear(std::string year, std::vector<double> dailySfAvg, std::vector<std::uint8_t> sfMonths);

    std::string getYear() { return m_year; }
    std::vector<double> getDailySfAvg() { return m_dailySfAvg; }
    std::vector<std::uint8_t> getCollapsedSfMonths() { return m_collapsedSfMonths; }
    std::vector<std::uint8_t> getSfMonths() { return m_sfMonths; }

    std::vector<double> getSfAverage() { return m_sfMonthlyAverages; }
    std::vector<double> getSfStdDev() { return m_sfMonthlyStdDevs; }

  private:
    const std::string m_year;
    std::vector<double> m_dailySfAvg;
    std::vector<std::uint8_t> m_sfMonths;

    std::vector<std::uint8_t> m_collapsedSfMonths;
    std::vector<double> m_sfMonthlyAverages;
    std::vector<double> m_sfMonthlyStdDevs;

    void computeSaveSfAverage();
    void computeSaveSfStdDev();
    void collapseSfMonths();
};
