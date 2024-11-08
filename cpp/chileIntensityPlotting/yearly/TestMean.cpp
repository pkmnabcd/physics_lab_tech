#include "mean.hpp"
#include "strTool.hpp"

#include <cmath>
#include <gtest/gtest.h>
#include <string>
#include <vector>

int main(int argc, char* argv[])
{
    testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}

TEST(getAverages, ComputesUnderNormalConditions)
{
    std::vector<double> timeData = { 1, 2, 3 };
    std::vector<double> tempData = { 1.5, 1.5, 1.5 };
    OneDay d1 = OneDay(timeData, tempData, 3);

    timeData = { 1, 2, 3, 4, 5 };
    tempData = { 3, 6, 1, 0, 2 };
    OneDay d2 = OneDay(timeData, tempData, 3);

    timeData = { 1, 2, 3, 4, 5 };
    tempData = { 2, 2, 2, 2, 2 };
    OneDay d3 = OneDay(timeData, tempData, 3);

    timeData = { 1, 2, 3, 4, 5 };
    tempData = { 2.0, 2.0, 2.0, 2.0, 2.0 };
    OneDay d4 = OneDay(timeData, tempData, 3);

    EXPECT_EQ(1.5, getAverage(d1));
    EXPECT_EQ(2.4, getAverage(d2));
    EXPECT_EQ(2, getAverage(d3));
    EXPECT_EQ(2, getAverage(d4));
}

TEST(getAverages, ComputesWithNan)
{
    std::vector<double> timeData = { 1, 2, 3 };
    std::vector<double> tempData = { 1.5, std::nan(""), 1.5 };
    OneDay d1 = OneDay(timeData, tempData, 3);

    timeData = { 1, 2, 3, 4, 5 };
    tempData = { 3, 6, 1, std::nan(""), 2 };
    OneDay d2 = OneDay(timeData, tempData, 3);

    timeData = { 1, 2, 3, 4, 5 };
    tempData = { 2, 2, 2, std::nan(""), 2 };
    OneDay d3 = OneDay(timeData, tempData, 3);

    EXPECT_EQ(1.5, getAverage(d1));
    EXPECT_EQ(3, getAverage(d2));
    EXPECT_EQ(2, getAverage(d3));
}

TEST(getAverages, AllNanReturnsNan)
{
    std::vector<double> timeData = { 1, 2, 3, 4, 5 };
    std::vector<double> tempData = { std::nan(""), std::nan(""), std::nan(""), std::nan(""), std::nan("") };
    OneDay d4 = OneDay(timeData, tempData, 3);

    EXPECT_TRUE(std::isnan(getAverage(d4)));
}

TEST(parseDoyFromFilename, GetsCorrectNumberNormal)
{
    std::string filename = "OH_Andover_ALO10day64.dat";
    EXPECT_EQ(64, parseDoyFromFilename(filename));
    filename = "OH_Andover_ALO10day2.dat";
    EXPECT_EQ(2, parseDoyFromFilename(filename));
    filename = "OH_Andover_ALO10day366.dat";
    EXPECT_EQ(366, parseDoyFromFilename(filename));
}

TEST(parseDoyFromFilename, GetsCorrectNumberDay1)
{
    std::string filename = "OH_Andover_ALO10day1.dat";
    EXPECT_EQ(366, parseDoyFromFilename(filename));
    filename = "OH_Andover_ALO13day1.dat";
    EXPECT_EQ(366, parseDoyFromFilename(filename));

    filename = "OH_Andover_ALO12day1.dat";
    EXPECT_EQ(367, parseDoyFromFilename(filename));
    filename = "OH_Andover_ALO24day1.dat";
    EXPECT_EQ(367, parseDoyFromFilename(filename));
}
