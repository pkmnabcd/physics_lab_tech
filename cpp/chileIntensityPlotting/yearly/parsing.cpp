#include "parsing.hpp"

#include "OneDay.hpp"

#include <filesystem>
#include <fstream>

OneDay parseOneDay(std::filesystem::path dayPath)
{
    std::ifstream file = std::ifstream(dayPath);

    auto tempReturn = std::vector<double>();
    return OneDay(tempReturn, tempReturn);
}
