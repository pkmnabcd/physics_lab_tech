#pragma once

#include "OneYear.hpp"

#include <string>
#include <vector>

bool writeAveragesToCSV(std::vector<OneYear>& yearAverages, std::string outputPathStr);
