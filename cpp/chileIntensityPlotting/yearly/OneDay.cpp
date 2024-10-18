#include "OneDay.hpp"

#include <vector>

OneDay::OneDay(std::vector<double> time, std::vector<double> OHTemp) :
    m_time(time),
    m_OHTemp(OHTemp)
{
}
