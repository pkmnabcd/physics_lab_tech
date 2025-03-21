#include "OneYear.hpp"

#include <cmath>
#include <cstdint>
#include <string>
#include <vector>

OneYear::OneYear(std::string year, std::vector<double> dailyOHAvg, std::vector<double> dailySfAvg, std::vector<std::uint8_t> ohMonths, std::vector<std::uint8_t> sfMonths) :
    m_year(year),
    m_dailyOHAvg(dailyOHAvg),
    m_dailySfAvg(dailySfAvg),
    m_ohMonths(ohMonths),
    m_sfMonths(sfMonths)
{
    computeSaveAverage();
    computeSaveStdDev();
    computeMonths();
}

// TODO: Fix these functions to work with the vectors of averages and stdevs and compute them monthly
void OneYear::computeSaveAverage()
{
    // TODO: It occurred to me that the number of OH days is less than the number of sf days, so I'll have to have separate average computations. Will need sf months and oh months. Either make a new function to separate the sf and oh computations or do it all here.
    std::uint8_t currentMonth = m_dailyMonths[0];
    std::uint8_t daysInMonth = 0;
    double ohTotal = 0;
    double sfTotal = 0;
    std::uint16_t ohNanCount = 0;
    std::uint16_t sfNanCount = 0;
    for (std::uint16_t i = 0; i < m_dailyMonths.size(); i++)
    {
        if (m_dailyMonths[i] == currentMonth)
        {
            daysInMonth++;
            double ohVal = m_dailyOHAvg[i];
            double sfVal = m_dailySolarAvg[i];
            if (std::isnan(ohVal))
            {
                ohNanCount++;
            }
            else
            {
                ohTotal += ohVal;
            }
            if (std::isnan(sfVal))
            {
                sfNanCount++;
            }
            else
            {
                ohTotal += sfVal;
            }
        }
        else
        {
            currentMonth = m_dailyMonths[i];
            daysInMonth = 0;
            ohTotal = 0;
            sfTotal = 0;
            ohNanCount = 0;
            sfNanCount = 0;

            double ohAvg = ohTotal / (daysInMonth - ohNanCount);
            double sfAvg = sfTotal / (daysInMonth - sfNanCount);
            m_OHMonthlyAverages.push_back(ohAvg);
            m_SolarMonthlyAverages.push_back(sfAvg);
        }
        // NOTE: Make sure to compute the last month's average and add it after the loop
    }

    // NOTE: computing OH average
    double total = 0;
    std::vector<double> temperature = m_dailyOHAvg;
    std::uint16_t nanCount = 0;
    for (auto& val : temperature)
    {
        if (std::isnan(val))
        {
            nanCount++;
            continue;
        }
        total += val;
    }
    double average = total / (temperature.size() - nanCount);
    m_OHAverage = average;

    // NOTE: computing solar flux average
    total = 0;
    std::vector<double> solarFlux = m_dailySolarAvg;
    nanCount = 0;
    for (auto& val : solarFlux)
    {
        if (std::isnan(val))
        {
            nanCount++;
            continue;
        }
        total += val;
    }
    average = total / (solarFlux.size() - nanCount);
    m_SolarAverage = average;
}

void OneYear::computeSaveStdDev()
{
    // NOTE: computing OH Temp standard deviation
    double mean = m_OHAverage;
    std::vector<double> OHTemp = m_dailyOHAvg;

    std::uint16_t numberOfVals = static_cast<std::uint16_t>(OHTemp.size());
    double summation = 0;

    for (double& val : OHTemp)
    {
        if (std::isnan(val))
        {
            numberOfVals--;
        }
        else
        {
            summation += pow((val - mean), 2);
        }
    }
    double stdDev = sqrt(summation / (numberOfVals - 1));
    m_OHStdDev = stdDev;

    // NOTE: computing solar flux standard deviation
    mean = m_SolarAverage;
    std::vector<double> solarFlux = m_dailySolarAvg;

    numberOfVals = static_cast<std::uint16_t>(solarFlux.size());
    summation = 0;

    for (double& val : solarFlux)
    {
        if (std::isnan(val))
        {
            numberOfVals--;
        }
        else
        {
            summation += pow((val - mean), 2);
        }
    }
    stdDev = sqrt(summation / (numberOfVals - 1));
    m_SolarStdDev = stdDev;
}

// TODO: Change this so that it uses the sf months since those are more consistent
void OneYear::computeMonths()
{
    for (std::uint8_t& currentMonth : m_dailyMonths)
    {
        bool present = false;
        for (std::uint8_t& month : m_months)
        {
            if (month == currentMonth)
            {
                present = true;
                break;
            }
        }
        if (!present)
        {
            m_months.push_back(currentMonth);
        }
    }
}
