#pragma once

#include <string>
#include <vector>

class OneYear
{
  public:
    OneYear(std::string year, std::vector<double> dailyOHAvg, std::vector<double> dailySolarAvg);

    std::string getYear() { return m_year; }
    std::vector<double> getDailyOHAvg() { return m_dailyOHAvg; }
    std::vector<double> getDailySolarAvg() { return m_dailySolarAvg; }

    double getOHAverage() { return m_OHAverage; }
    double getOHStdDev() { return m_OHStdDev; }
    double getSolarAverage() { return m_SolarAverage; }
    double getSolarStdDev() { return m_SolarStdDev; }

  private:
    const std::string m_year;
    std::vector<double> m_dailyOHAvg;
    std::vector<double> m_dailySolarAvg;

    double m_OHAverage;
    double m_OHStdDev;
    double m_SolarAverage;
    double m_SolarStdDev;

    void computeSaveAverage();
    void computeSaveStdDev();
};
