#include "OneDay.hpp"

#include <vector>

OneDay::OneDay(std::vector<double> time, std::vector<double> OHTemp, unsigned int dayOfYear) :
    m_time(time),
    m_OHTemp(OHTemp),
    m_dayOfYear(dayOfYear)
{
}
