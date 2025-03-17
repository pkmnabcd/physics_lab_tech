#include "OneDay.hpp"

#include <string>
#include <vector>

OneDay::OneDay(std::vector<double> time, std::vector<double> OHTemp, unsigned int dayOfYear, std::string month) :
    m_time(time),
    m_OHTemp(OHTemp),
    m_dayOfYear(dayOfYear),
    m_month(month)
{
}
