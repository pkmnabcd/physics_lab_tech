#pragma once

#include "OneDay.hpp"

#include <optional>
#include <string>
#include <vector>
std::vector<OneDay> getYearlyAverages(std::string year_path);

std::optional<double> calculateAverage(OneDay dayData, bool doingTest);
double calculateStdDev(OneDay dayData);

const std::vector<std::string> MONTH_HEADERS = {
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
};
