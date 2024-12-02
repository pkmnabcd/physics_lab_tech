#pragma once

#include "OneDay.hpp"

#include <string>
#include <vector>

bool writeAveragesToCSV(std::string yearPath, std::vector<OneDay>& yearAverages, std::string& outputPathStr);
