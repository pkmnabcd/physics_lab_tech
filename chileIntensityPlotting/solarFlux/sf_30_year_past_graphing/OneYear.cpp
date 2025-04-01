#include "OneYear.hpp"

#include <cassert>
#include <cmath>
#include <cstdint>
#include <string>
#include <vector>

OneYear::OneYear(std::string year, std::vector<double> dailySfAvg, std::vector<std::uint8_t> sfMonths) :
    m_year(year),
    m_dailySfAvg(dailySfAvg),
    m_sfMonths(sfMonths)
{
    computeSaveSfAverage();
    computeSaveSfStdDev();
    collapseSfMonths();
}

void OneYear::computeSaveSfAverage()
{
    std::uint8_t currentMonth = m_sfMonths[0];
    std::uint8_t daysInMonth = 0;
    double total = 0;
    std::uint16_t nanCount = 0;
    for (std::uint16_t i = 0; i < m_sfMonths.size(); i++)
    {
        if (m_sfMonths[i] == currentMonth)
        {
            daysInMonth++;
            double val = m_dailySfAvg[i];
            if (std::isnan(val))
            {
                nanCount++;
            }
            else
            {
                total += val;
            }
        }
        else
        {
            double avg = total / (daysInMonth - nanCount);
            m_sfMonthlyAverages.push_back(avg);

            // NOTE: reset the month
            currentMonth = m_sfMonths[i];
            daysInMonth = 0;
            total = 0;
            nanCount = 0;

            daysInMonth++;
            double val = m_dailySfAvg[i];
            if (std::isnan(val))
            {
                nanCount++;
            }
            else
            {
                total += val;
            }
        }
    }
    // NOTE: adding the last average
    double avg = total / (daysInMonth - nanCount);
    m_sfMonthlyAverages.push_back(avg);
}

void OneYear::computeSaveSfStdDev()
{
    std::uint8_t currentMonth = m_sfMonths[0];
    std::uint8_t daysInMonth = 0;
    double summation = 0;
    std::uint8_t meanIndex = 0;
    double mean = m_sfMonthlyAverages[meanIndex];
    std::uint16_t nanCount = 0;
    for (std::uint16_t i = 0; i < m_sfMonths.size(); i++)
    {
        if (m_sfMonths[i] == currentMonth)
        {
            daysInMonth++;
            double val = m_dailySfAvg[i];
            if (std::isnan(val))
            {
                nanCount++;
            }
            else
            {
                summation += pow((val - mean), 2);
            }
        }
        else
        {
            double stdDev = sqrt(summation / ((daysInMonth - nanCount) - 1));
            m_sfMonthlyStdDevs.push_back(stdDev);

            // NOTE: Reset month
            currentMonth = m_sfMonths[i];
            meanIndex++;
            mean = m_sfMonthlyAverages[meanIndex];
            daysInMonth = 0;
            summation = 0;
            nanCount = 0;

            daysInMonth++;
            double val = m_dailySfAvg[i];
            if (std::isnan(val))
            {
                nanCount++;
            }
            else
            {
                summation += pow((val - mean), 2);
            }
        }
    }
    // NOTE: adding the last standard deviation
    double stdDev = sqrt(summation / ((daysInMonth - nanCount) - 1));
    m_sfMonthlyStdDevs.push_back(stdDev);
}

void OneYear::collapseSfMonths()
{
    for (std::uint8_t& currentMonth : m_sfMonths)
    {
        bool present = false;
        for (std::uint8_t& month : m_collapsedSfMonths)
        {
            if (month == currentMonth)
            {
                present = true;
                break;
            }
        }
        if (!present)
        {
            m_collapsedSfMonths.push_back(currentMonth);
        }
    }
    assert(m_collapsedSfMonths.size() == m_sfMonthlyAverages.size() && "Same number of months as averages");
    assert(m_collapsedSfMonths.size() == m_sfMonthlyStdDevs.size() && "Same number of months as std devs");
}
