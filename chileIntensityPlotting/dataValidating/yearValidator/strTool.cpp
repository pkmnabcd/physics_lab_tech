#include "strTool.hpp"

#include <cassert>
#include <string>

bool isNumeric(std::string input)
{
    for (unsigned int i = 0; i < input.length(); i++)
    {
        if (!std::isdigit(input.at(i)))
        {
            return false;
        }
    }
    return true;
}

std::string getYearFromPath(std::string yearPathStr)
{
    std::string year;
    if (std::string::npos != yearPathStr.find('/'))
    {
        auto position = yearPathStr.find_last_of('/');
        if (position == yearPathStr.length() - 1)
        {
            yearPathStr = yearPathStr.substr(0, yearPathStr.length() - 1);
            position = yearPathStr.find_last_of('/');
        }
        year = yearPathStr.substr(position + 1);
    }
    else
    {
        year = yearPathStr;
    }
    assert(isNumeric(year));
    return year;
}

unsigned int parseDoyFromFilename(std::string filename)
{
    auto doyStartPosition = filename.find('y') + 1;
    auto doyEndPosition = filename.find('.') - 1;
    auto positionDelta = doyEndPosition - doyStartPosition;
    std::string doyStr = "";
    for (unsigned int i = 0; i <= positionDelta; i++)
    {
        doyStr += filename[doyStartPosition + i];
    }
    unsigned int doy = std::stoi(doyStr);
    if (doy == 1)
    {
        std::string::size_type yearStartPosition = filename.find("ALO") + 3;
        std::string yearStr = "";
        yearStr += filename[yearStartPosition];
        yearStr += filename[yearStartPosition + 1];
        unsigned int year = std::stoi(yearStr);
        if (year % 4 == 0)
        {
            doy = 367;
        }
        else
        {
            doy = 366;
        }
    }
    return doy;
}

std::uint32_t parseBinary(char* buffer, std::uint8_t size)
{
    std::uint32_t output = 0;
    while (size > 0)
    {
        std::uint8_t i = size - 1;
        output |= (static_cast<std::uint32_t>(buffer[i]) << (8 * i));
        size--;
    }

    return output;
}
