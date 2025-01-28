#pragma once

#include "OneDay.hpp"
#include "OneYear.hpp"

#include <cstdint>
#include <optional>
#include <string>
#include <vector>
OneYear getYearAverages(std::string year);

std::optional<double> calculateAverage(OneDay dayData, bool doingTest, std::string year);
double calculateStdDev(OneDay dayData);

std::uint8_t getHourLength(OneDay day, std::string yearStr);

const std::vector<std::string> MONTH_HEADERS = {
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
};
