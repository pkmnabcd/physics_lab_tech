#pragma once

#include "OneDay.hpp"

#include <filesystem>

// This isn't the best way to do it, but I wanted to practice writing classes for a course.
OneDay parseOneDay(std::filesystem::path dayPath);
