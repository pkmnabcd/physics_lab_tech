#pragma once

#include <string>
#include <vector>
std::vector<std::vector<double>> getYearlyAverages(std::string year_path);

const std::vector<std::string> MONTH_HEADERS = {
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
};
