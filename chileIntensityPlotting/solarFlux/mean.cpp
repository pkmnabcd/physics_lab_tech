#include "mean.hpp"

#include "OneYear.hpp"
#include "parsing.hpp"
#include "strTool.hpp"

#include <filesystem>
#include <print>
#include <string>
#include <vector>

OneYear getYearAverages(std::string year)
{
    auto yearPath = std::filesystem::path(year);

    OneYear yearlyAverages("test", { 1.3, 4.5 }, { 3, 4.1 });
    return yearlyAverages;
}
