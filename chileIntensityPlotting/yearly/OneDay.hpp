#pragma once

#include <vector>

class OneDay
{
  public:
    OneDay(std::vector<double> time, std::vector<double> OHTemp, unsigned int dayOfYear);

    std::vector<double> getTime() { return m_time; }
    std::vector<double> getOHTemp() { return m_OHTemp; }
    unsigned int getDayOfYear() { return m_dayOfYear; }

  private:
    const std::vector<double> m_time;
    const std::vector<double> m_OHTemp;
    const unsigned int m_dayOfYear;
};
