#pragma once

#include "OneDay.hpp"

#include <filesystem>
#include <string>

OneDay parseOneDay(std::filesystem::path dayPath, std::string month);
