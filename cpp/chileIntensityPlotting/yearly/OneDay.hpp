#pragma once

#include <vector>

class OneDay
{
  public:
    OneDay(std::vector<double> time, std::vector<double> OHTemp);

    std::vector<double> getTime() { return m_time; }
    std::vector<double> getOHTemp() { return m_OHTemp; }

  private:
    const std::vector<double> m_time;
    const std::vector<double> m_OHTemp;
};
