#pragma once

#include <cstdint>
#include <string>

std::string getYearFromPath(std::string yearPathStr);
unsigned int parseDoyFromFilename(std::string filename);
std::uint32_t parseBinary(char* buffer, std::uint8_t size);
