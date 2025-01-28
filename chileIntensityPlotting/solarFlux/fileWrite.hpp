#pragma once

#include "OneDay.hpp"
#include "OneYear.hpp"

#include <string>
#include <vector>

bool writeAveragesToCSV(std::string yearPath, std::vector<OneYear>& yearAverages, std::string& outputPathStr);
