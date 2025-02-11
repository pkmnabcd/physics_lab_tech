#pragma once

#include <vector>

class OneDay
{
  public:
    OneDay(std::vector<double> darkIntensity, unsigned int dayOfYear);

    std::vector<double> getDarkIntensity() { return m_darkIntensity; }
    unsigned int getDayOfYear() { return m_dayOfYear; }

  private:
    std::vector<double> m_darkIntensity;
    const unsigned int m_dayOfYear;
};
