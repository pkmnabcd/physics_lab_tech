#include "OneYear.hpp"

#include <cassert>
#include <cmath>
#include <cstdint>
#include <string>
#include <vector>

OneYear::OneYear(std::string year, std::vector<double> dailyOHAvg, std::vector<double> dailySfAvg, std::vector<std::uint8_t> OHMonths, std::vector<std::uint8_t> sfMonths) :
    m_year(year),
    m_dailyOHAvg(dailyOHAvg),
    m_dailySfAvg(dailySfAvg),
    m_OHMonths(OHMonths),
    m_sfMonths(sfMonths)
{
    computeSaveOHAverage();
    computeSaveSfAverage();
    computeSaveOHStdDev();
    computeSaveSfStdDev();
    collapseOHMonths();
    collapseSfMonths();
}

void OneYear::computeSaveOHAverage()
{
    std::uint8_t currentMonth = m_OHMonths[0];
    std::uint8_t daysInMonth = 0;
    double total = 0;
    std::uint16_t nanCount = 0;
    for (std::uint16_t i = 0; i < m_OHMonths.size(); i++)
    {
        if (m_OHMonths[i] == currentMonth)
        {
            daysInMonth++;
            double val = m_dailyOHAvg[i];
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
            m_OHMonthlyAverages.push_back(avg);

            currentMonth = m_OHMonths[i];
            daysInMonth = 0;
            total = 0;
            nanCount = 0;
        }
    }
    // NOTE: adding the last average
    double avg = total / (daysInMonth - nanCount);
    m_OHMonthlyAverages.push_back(avg);
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

            currentMonth = m_sfMonths[i];
            daysInMonth = 0;
            total = 0;
            nanCount = 0;
        }
    }
    // NOTE: adding the last average
    double avg = total / (daysInMonth - nanCount);
    m_sfMonthlyAverages.push_back(avg);
}

void OneYear::computeSaveOHStdDev()
{
    std::uint8_t currentMonth = m_OHMonths[0];
    std::uint8_t daysInMonth = 0;
    double summation = 0;
    double mean = m_OHMonthlyAverages[0];
    std::uint16_t nanCount = 0;
    for (std::uint16_t i = 0; i < m_OHMonths.size(); i++)
    {
        if (m_OHMonths[i] == currentMonth)
        {
            daysInMonth++;
            double val = m_dailyOHAvg[i];
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
            m_OHMonthlyStdDevs.push_back(stdDev);

            currentMonth = m_OHMonths[i];
            mean = m_OHMonthlyAverages[i];
            daysInMonth = 0;
            summation = 0;
            nanCount = 0;
        }
    }
    // NOTE: adding the last standard deviation
    double stdDev = sqrt(summation / ((daysInMonth - nanCount) - 1));
    m_OHMonthlyStdDevs.push_back(stdDev);
}

void OneYear::computeSaveSfStdDev()
{
    std::uint8_t currentMonth = m_sfMonths[0];
    std::uint8_t daysInMonth = 0;
    double summation = 0;
    double mean = m_sfMonthlyAverages[0];
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

            currentMonth = m_sfMonths[i];
            mean = m_sfMonthlyAverages[i];
            daysInMonth = 0;
            summation = 0;
            nanCount = 0;
        }
    }
    // NOTE: adding the last standard deviation
    double stdDev = sqrt(summation / ((daysInMonth - nanCount) - 1));
    m_sfMonthlyStdDevs.push_back(stdDev);
}

void OneYear::collapseOHMonths()
{
    for (std::uint8_t& currentMonth : m_OHMonths)
    {
        bool present = false;
        for (std::uint8_t& month : m_collapsedOHMonths)
        {
            if (month == currentMonth)
            {
                present = true;
                break;
            }
        }
        if (!present)
        {
            m_collapsedOHMonths.push_back(currentMonth);
        }
    }
    assert(m_collapsedOHMonths.size() == m_OHMonthlyAverages.size() && "Same number of months as averages")
    assert(m_collapsedOHMonths.size() == m_OHMonthlyStdDevs.size() && "Same number of months as std devs")
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
    assert(m_collapsedSfMonths.size() == m_SfMonthlyAverages.size() && "Same number of months as averages")
    assert(m_collapsedSfMonths.size() == m_SfMonthlyStdDevs.size() && "Same number of months as std devs")
}
