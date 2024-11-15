#pragma once

#include "OneDay.hpp"

#include <string>
#include <vector>
std::vector<OneDay> getYearlyAverages(std::string year_path);

double getAverage(OneDay dayData);
double getStdDev(OneDay dayData);

const std::vector<std::string> MONTH_HEADERS = {
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
};
