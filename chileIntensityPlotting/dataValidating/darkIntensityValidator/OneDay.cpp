#include "OneDay.hpp"

#include <vector>

OneDay::OneDay(std::vector<double> darkIntensity, unsigned int dayOfYear) :
    m_darkIntensity(darkIntensity),
    m_dayOfYear(dayOfYear)
{
}
