#pragma once

#include "OneYear.hpp"

#include <cstdint>
#include <string>
#include <vector>

std::vector<std::string> split(std::string input, std::uint8_t ch);
OneYear parseOneYear(std::string year);
