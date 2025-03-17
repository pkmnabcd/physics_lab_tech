#pragma once

#include <string>
#include <vector>

class OneDay
{
  public:
    OneDay(std::vector<double> time, std::vector<double> OHTemp, unsigned int dayOfYear, std::string month);

    std::vector<double> getTime() { return m_time; }
    std::vector<double> getOHTemp() { return m_OHTemp; }
    unsigned int getDayOfYear() { return m_dayOfYear; }
    std::string getMonth() { return m_month; }
    double getAverage() { return m_average; }
    double getStdDev() { return m_stdDev; }

    void setTime(std::vector<double> newTime) { m_time = newTime; }
    void setOHTemp(std::vector<double> newOH) { m_OHTemp = newOH; }
    void setAverage(double average) { m_average = average; }
    void setStdDev(double stdDev) { m_stdDev = stdDev; }

  private:
    std::vector<double> m_time;
    std::vector<double> m_OHTemp;
    const unsigned int m_dayOfYear;
    const std::string m_month;
    double m_average;
    double m_stdDev;
};
