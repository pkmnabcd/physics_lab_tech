#include "OneYear.hpp"

#include <cmath>
#include <cstdint>
#include <string>
#include <vector>

OneYear::OneYear(std::string year, std::vector<double> dailyOHAvg, std::vector<double> dailySolarAvg, std::vector<std::uint8_t> months) :
    m_year(year),
    m_dailyOHAvg(dailyOHAvg),
    m_dailySolarAvg(dailySolarAvg),
    m_months(months)
{
    computeSaveAverage();
    computeSaveStdDev();
}

// TODO: Fix these functions to work with the vectors of averages and stdevs and compute them monthly
void OneYear::computeSaveAverage()
{
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
