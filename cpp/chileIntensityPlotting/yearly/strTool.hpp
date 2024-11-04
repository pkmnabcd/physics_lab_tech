#pragma once

#include <string>

bool isNumeric(std::string input);
std::string getYearFromPath(std::string yearPathStr);
unsigned int parseDoyFromFilename(std::string filename);
