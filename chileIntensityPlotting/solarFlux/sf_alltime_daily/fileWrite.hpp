#pragma once

#include "SolarFluxData.hpp"

#include <string>

bool writeAveragesToCSV(SolarFluxData& sfData, std::string outputPathStr);
