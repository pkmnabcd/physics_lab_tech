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
        std::cout << line << std::endl;
        lineNumber++;
    }

    unsigned int lineLength = headerLine.length();
    unsigned int colLength = 15;
    unsigned int numberOfColumns = lineLength / colLength;
    if (numberOfColumns != 8)
    {
        std::cout << "Warning! Number of Columns is wrong for " << dayPath << "!\nExpected 8 and got " << numberOfColumns << std::endl;
    }
    std::vector<double> timeData = std::vector<double>();
    std::vector<double> tempData = std::vector<double>();

    for (std::string line : lines)
    {
        for (unsigned int i = 0; i < 2; i++) // Just want the first two columns
        {
            unsigned int indexStart = i * colLength;
            std::string substring = line.substr(indexStart, colLength);

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
            if (i == 0)
            {
                timeData.push_back(addVal);
            }
            else if (i == 1)
            {
                tempData.push_back(addVal);
            }
        }
    }
    for (unsigned int i = 0; i < timeData.size(); i++)
    {
        std::cout << timeData[i] << " : " << tempData[i] << std::endl;
    }

    file.close();

    return OneDay(timeData, tempData, doy);
}
