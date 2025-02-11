#include "parsing.hpp"

#include "OneDay.hpp"
#include "strTool.hpp"

#include <cmath>
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
    std::string headerLine;
    unsigned int lineNumber = 1;
    while (std::getline(file, line))
    {
        if (lineNumber == 1)
        {
            headerLine = line;
        }
        else
        {
            lines.push_back(line);
        }
        lineNumber++;
    }

    unsigned int lineLength = static_cast<unsigned int>(headerLine.length());
    unsigned int colLength = 15;
    unsigned int numberOfColumns = lineLength / colLength;
    if (numberOfColumns != 8)
    {
        std::cout << "Warning! Number of Columns is wrong for " << dayPath << "!\nExpected 8 and got " << numberOfColumns << std::endl;
    }
    std::vector<double> darkData = std::vector<double>();

    for (std::string currentLine : lines)
    {
        unsigned int indexStart = 7 * colLength; // Just want last column
        std::string substring = currentLine.substr(indexStart, colLength);

        std::string::size_type spacePos = substring.find(" ");
        while (spacePos != std::string::npos)
        {
            substring = substring.substr(spacePos + 1, substring.size() - 1);
            spacePos = substring.find(" ");
        }
        double addVal;
        if (substring.contains("*"))
        {
            addVal = std::nan("");
        }
        else if (substring.contains("NaN"))
        {
            addVal = std::nan("");
        }
        else
        {
            addVal = std::stod(substring);
        }
        darkData.push_back(addVal);
    }
    file.close();

    return OneDay(darkData, doy);
}
