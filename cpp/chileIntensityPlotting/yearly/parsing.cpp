#include "parsing.hpp"

#include "OneDay.hpp"
#include "strTool.hpp"

#include <filesystem>
#include <fstream>
#include <iostream>
#include <vector>

OneDay parseOneDay(std::filesystem::path dayPath)
{
    unsigned int doy = parseDoyFromFilename(dayPath.filename().string());

    std::ifstream file = std::ifstream(dayPath);
    std::vector<std::string> lines;
    std::string line;
    while (std::getline(file, line))
    {
        std::cout << line << std::endl;
    }
    file.close();

    auto tempReturn = std::vector<double>();
    return OneDay(tempReturn, tempReturn, doy);
}
