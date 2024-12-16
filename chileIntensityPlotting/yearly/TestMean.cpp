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

TEST(calculateAverages, ComputesUnderNormalConditions)
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

    EXPECT_EQ(1.5, calculateAverage(d1, true, "2020").value());
    EXPECT_EQ(2.4, calculateAverage(d2, true, "2020").value());
    EXPECT_EQ(2, calculateAverage(d3, true, "2020").value());
    EXPECT_EQ(2, calculateAverage(d4, true, "2020").value());
}

TEST(calculateAverages, ComputesWithNan)
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

    EXPECT_EQ(1.5, calculateAverage(d1, true, "2020").value());
    EXPECT_EQ(3, calculateAverage(d2, true, "2020").value());
    EXPECT_EQ(2, calculateAverage(d3, true, "2020").value());
}

TEST(calculateAverages, AllNanReturnsNan)
{
    std::vector<double> timeData = { 1, 2, 3, 4, 5 };
    std::vector<double> tempData = { std::nan(""), std::nan(""), std::nan(""), std::nan(""), std::nan("") };
    OneDay d4 = OneDay(timeData, tempData, 3);

    EXPECT_TRUE(std::isnan(calculateAverage(d4, true, "2020").value()));
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

TEST(getHourLength, worksFor2009)
{
    std::string year = "2009";

    OneDay d1 = OneDay({}, {}, 2);
    OneDay d2 = OneDay({}, {}, 100);
    OneDay d3 = OneDay({}, {}, 200);
    OneDay d4 = OneDay({}, {}, 280);
    OneDay d5 = OneDay({}, {}, 281);
    OneDay d6 = OneDay({}, {}, 282);
    OneDay d7 = OneDay({}, {}, 300);
    OneDay d8 = OneDay({}, {}, 318);
    OneDay d9 = OneDay({}, {}, 319);
    OneDay d10 = OneDay({}, {}, 320);
    OneDay d11 = OneDay({}, {}, 363);
    OneDay d12 = OneDay({}, {}, 365);
    OneDay d13 = OneDay({}, {}, 1);

    EXPECT_EQ(10, getHourLength(d1, year));
    EXPECT_EQ(10, getHourLength(d2, year));
    EXPECT_EQ(10, getHourLength(d3, year));
    EXPECT_EQ(10, getHourLength(d4, year));
    EXPECT_EQ(10, getHourLength(d5, year));
    EXPECT_EQ(10, getHourLength(d6, year));
    EXPECT_EQ(10, getHourLength(d7, year));
    EXPECT_EQ(10, getHourLength(d8, year));
    EXPECT_EQ(10, getHourLength(d9, year));
    EXPECT_EQ(10, getHourLength(d10, year));
    EXPECT_EQ(10, getHourLength(d11, year));
    EXPECT_EQ(10, getHourLength(d12, year));
    EXPECT_EQ(10, getHourLength(d13, year));
}

TEST(getHourLength, worksFor2010)
{
    std::string year = "2010";

    OneDay d1 = OneDay({}, {}, 2);
    OneDay d2 = OneDay({}, {}, 100);
    OneDay d3 = OneDay({}, {}, 200);
    OneDay d4 = OneDay({}, {}, 280);
    OneDay d5 = OneDay({}, {}, 281);
    OneDay d6 = OneDay({}, {}, 282);
    OneDay d7 = OneDay({}, {}, 300);
    OneDay d8 = OneDay({}, {}, 318);
    OneDay d9 = OneDay({}, {}, 319);
    OneDay d10 = OneDay({}, {}, 320);
    OneDay d11 = OneDay({}, {}, 363);
    OneDay d12 = OneDay({}, {}, 365);
    OneDay d13 = OneDay({}, {}, 1);

    EXPECT_EQ(10, getHourLength(d1, year));
    EXPECT_EQ(10, getHourLength(d2, year));
    EXPECT_EQ(10, getHourLength(d3, year));
    EXPECT_EQ(10, getHourLength(d4, year));
    EXPECT_EQ(10, getHourLength(d5, year));
    EXPECT_EQ(10, getHourLength(d6, year));
    EXPECT_EQ(10, getHourLength(d7, year));
    EXPECT_EQ(10, getHourLength(d8, year));
    EXPECT_EQ(10, getHourLength(d9, year));
    EXPECT_EQ(10, getHourLength(d10, year));
    EXPECT_EQ(10, getHourLength(d11, year));
    EXPECT_EQ(10, getHourLength(d12, year));
    EXPECT_EQ(10, getHourLength(d13, year));
}

TEST(getHourLength, worksFor2011)
{
    std::string year = "2011";

    OneDay d1 = OneDay({}, {}, 2);
    OneDay d2 = OneDay({}, {}, 100);
    OneDay d3 = OneDay({}, {}, 200);
    OneDay d4 = OneDay({}, {}, 280);
    OneDay d5 = OneDay({}, {}, 281);
    OneDay d6 = OneDay({}, {}, 282);
    OneDay d7 = OneDay({}, {}, 300);
    OneDay d8 = OneDay({}, {}, 318);
    OneDay d9 = OneDay({}, {}, 319);
    OneDay d10 = OneDay({}, {}, 320);
    OneDay d11 = OneDay({}, {}, 363);
    OneDay d12 = OneDay({}, {}, 365);
    OneDay d13 = OneDay({}, {}, 1);

    EXPECT_EQ(10, getHourLength(d1, year));
    EXPECT_EQ(10, getHourLength(d2, year));
    EXPECT_EQ(10, getHourLength(d3, year));
    EXPECT_EQ(10, getHourLength(d4, year));
    EXPECT_EQ(10, getHourLength(d5, year));
    EXPECT_EQ(10, getHourLength(d6, year));
    EXPECT_EQ(10, getHourLength(d7, year));
    EXPECT_EQ(10, getHourLength(d8, year));
    EXPECT_EQ(33, getHourLength(d9, year));
    EXPECT_EQ(33, getHourLength(d10, year));
    EXPECT_EQ(33, getHourLength(d11, year));
    EXPECT_EQ(33, getHourLength(d12, year));
    EXPECT_EQ(33, getHourLength(d13, year));
}

TEST(getHourLength, worksFor2012)
{
    std::string year = "2012";

    OneDay d1 = OneDay({}, {}, 2);
    OneDay d2 = OneDay({}, {}, 100);
    OneDay d3 = OneDay({}, {}, 200);
    OneDay d4 = OneDay({}, {}, 280);
    OneDay d5 = OneDay({}, {}, 281);
    OneDay d6 = OneDay({}, {}, 282);
    OneDay d7 = OneDay({}, {}, 300);
    OneDay d8 = OneDay({}, {}, 318);
    OneDay d9 = OneDay({}, {}, 319);
    OneDay d10 = OneDay({}, {}, 320);
    OneDay d11 = OneDay({}, {}, 363);
    OneDay d12 = OneDay({}, {}, 365);
    OneDay d13 = OneDay({}, {}, 1);

    EXPECT_EQ(33, getHourLength(d1, year));
    EXPECT_EQ(33, getHourLength(d2, year));
    EXPECT_EQ(33, getHourLength(d3, year));
    EXPECT_EQ(33, getHourLength(d4, year));
    EXPECT_EQ(33, getHourLength(d5, year));
    EXPECT_EQ(33, getHourLength(d6, year));
    EXPECT_EQ(33, getHourLength(d7, year));
    EXPECT_EQ(33, getHourLength(d8, year));
    EXPECT_EQ(33, getHourLength(d9, year));
    EXPECT_EQ(33, getHourLength(d10, year));
    EXPECT_EQ(33, getHourLength(d11, year));
    EXPECT_EQ(33, getHourLength(d12, year));
    EXPECT_EQ(33, getHourLength(d13, year));
}

TEST(getHourLength, worksFor2013)
{
    std::string year = "2013";

    OneDay d1 = OneDay({}, {}, 2);
    OneDay d2 = OneDay({}, {}, 100);
    OneDay d3 = OneDay({}, {}, 200);
    OneDay d4 = OneDay({}, {}, 280);
    OneDay d5 = OneDay({}, {}, 281);
    OneDay d6 = OneDay({}, {}, 282);
    OneDay d7 = OneDay({}, {}, 300);
    OneDay d8 = OneDay({}, {}, 318);
    OneDay d9 = OneDay({}, {}, 319);
    OneDay d10 = OneDay({}, {}, 320);
    OneDay d11 = OneDay({}, {}, 363);
    OneDay d12 = OneDay({}, {}, 365);
    OneDay d13 = OneDay({}, {}, 1);

    EXPECT_EQ(33, getHourLength(d1, year));
    EXPECT_EQ(33, getHourLength(d2, year));
    EXPECT_EQ(33, getHourLength(d3, year));
    EXPECT_EQ(33, getHourLength(d4, year));
    EXPECT_EQ(33, getHourLength(d5, year));
    EXPECT_EQ(33, getHourLength(d6, year));
    EXPECT_EQ(33, getHourLength(d7, year));
    EXPECT_EQ(33, getHourLength(d8, year));
    EXPECT_EQ(33, getHourLength(d9, year));
    EXPECT_EQ(33, getHourLength(d10, year));
    EXPECT_EQ(33, getHourLength(d11, year));
    EXPECT_EQ(33, getHourLength(d12, year));
    EXPECT_EQ(33, getHourLength(d13, year));
}

TEST(getHourLength, worksFor2014)
{
    std::string year = "2014";

    OneDay d1 = OneDay({}, {}, 2);
    OneDay d2 = OneDay({}, {}, 100);
    OneDay d3 = OneDay({}, {}, 200);
    OneDay d4 = OneDay({}, {}, 280);
    OneDay d5 = OneDay({}, {}, 281);
    OneDay d6 = OneDay({}, {}, 282);
    OneDay d7 = OneDay({}, {}, 300);
    OneDay d8 = OneDay({}, {}, 318);
    OneDay d9 = OneDay({}, {}, 319);
    OneDay d10 = OneDay({}, {}, 320);
    OneDay d11 = OneDay({}, {}, 363);
    OneDay d12 = OneDay({}, {}, 365);
    OneDay d13 = OneDay({}, {}, 1);

    EXPECT_EQ(33, getHourLength(d1, year));
    EXPECT_EQ(33, getHourLength(d2, year));
    EXPECT_EQ(33, getHourLength(d3, year));
    EXPECT_EQ(33, getHourLength(d4, year));
    EXPECT_EQ(33, getHourLength(d5, year));
    EXPECT_EQ(33, getHourLength(d6, year));
    EXPECT_EQ(33, getHourLength(d7, year));
    EXPECT_EQ(33, getHourLength(d8, year));
    EXPECT_EQ(33, getHourLength(d9, year));
    EXPECT_EQ(33, getHourLength(d10, year));
    EXPECT_EQ(33, getHourLength(d11, year));
    EXPECT_EQ(33, getHourLength(d12, year));
    EXPECT_EQ(33, getHourLength(d13, year));
}

TEST(getHourLength, worksFor2015)
{
    std::string year = "2015";

    OneDay d1 = OneDay({}, {}, 2);
    OneDay d2 = OneDay({}, {}, 100);
    OneDay d3 = OneDay({}, {}, 200);
    OneDay d4 = OneDay({}, {}, 280);
    OneDay d5 = OneDay({}, {}, 281);
    OneDay d6 = OneDay({}, {}, 282);
    OneDay d7 = OneDay({}, {}, 300);
    OneDay d8 = OneDay({}, {}, 318);
    OneDay d9 = OneDay({}, {}, 319);
    OneDay d10 = OneDay({}, {}, 320);
    OneDay d11 = OneDay({}, {}, 363);
    OneDay d12 = OneDay({}, {}, 365);
    OneDay d13 = OneDay({}, {}, 1);

    EXPECT_EQ(33, getHourLength(d1, year));
    EXPECT_EQ(33, getHourLength(d2, year));
    EXPECT_EQ(33, getHourLength(d3, year));
    EXPECT_EQ(33, getHourLength(d4, year));
    EXPECT_EQ(33, getHourLength(d5, year));
    EXPECT_EQ(33, getHourLength(d6, year));
    EXPECT_EQ(33, getHourLength(d7, year));
    EXPECT_EQ(33, getHourLength(d8, year));
    EXPECT_EQ(33, getHourLength(d9, year));
    EXPECT_EQ(33, getHourLength(d10, year));
    EXPECT_EQ(33, getHourLength(d11, year));
    EXPECT_EQ(33, getHourLength(d12, year));
    EXPECT_EQ(33, getHourLength(d13, year));
}

TEST(getHourLength, worksFor2016)
{
    std::string year = "2016";

    OneDay d1 = OneDay({}, {}, 2);
    OneDay d2 = OneDay({}, {}, 100);
    OneDay d3 = OneDay({}, {}, 200);
    OneDay d4 = OneDay({}, {}, 280);
    OneDay d5 = OneDay({}, {}, 281);
    OneDay d6 = OneDay({}, {}, 282);
    OneDay d7 = OneDay({}, {}, 300);
    OneDay d8 = OneDay({}, {}, 318);
    OneDay d9 = OneDay({}, {}, 319);
    OneDay d10 = OneDay({}, {}, 320);
    OneDay d11 = OneDay({}, {}, 363);
    OneDay d12 = OneDay({}, {}, 365);
    OneDay d13 = OneDay({}, {}, 1);

    EXPECT_EQ(33, getHourLength(d1, year));
    EXPECT_EQ(33, getHourLength(d2, year));
    EXPECT_EQ(33, getHourLength(d3, year));
    EXPECT_EQ(33, getHourLength(d4, year));
    EXPECT_EQ(33, getHourLength(d5, year));
    EXPECT_EQ(33, getHourLength(d6, year));
    EXPECT_EQ(33, getHourLength(d7, year));
    EXPECT_EQ(33, getHourLength(d8, year));
    EXPECT_EQ(33, getHourLength(d9, year));
    EXPECT_EQ(33, getHourLength(d10, year));
    EXPECT_EQ(33, getHourLength(d11, year));
    EXPECT_EQ(33, getHourLength(d12, year));
    EXPECT_EQ(33, getHourLength(d13, year));
}

TEST(getHourLength, worksFor2017)
{
    std::string year = "2017";

    OneDay d1 = OneDay({}, {}, 2);
    OneDay d2 = OneDay({}, {}, 100);
    OneDay d3 = OneDay({}, {}, 200);
    OneDay d4 = OneDay({}, {}, 280);
    OneDay d5 = OneDay({}, {}, 281);
    OneDay d6 = OneDay({}, {}, 282);
    OneDay d7 = OneDay({}, {}, 300);
    OneDay d8 = OneDay({}, {}, 318);
    OneDay d9 = OneDay({}, {}, 319);
    OneDay d10 = OneDay({}, {}, 320);
    OneDay d11 = OneDay({}, {}, 363);
    OneDay d12 = OneDay({}, {}, 365);
    OneDay d13 = OneDay({}, {}, 1);

    EXPECT_EQ(33, getHourLength(d1, year));
    EXPECT_EQ(33, getHourLength(d2, year));
    EXPECT_EQ(33, getHourLength(d3, year));
    EXPECT_EQ(33, getHourLength(d4, year));
    EXPECT_EQ(33, getHourLength(d5, year));
    EXPECT_EQ(33, getHourLength(d6, year));
    EXPECT_EQ(33, getHourLength(d7, year));
    EXPECT_EQ(33, getHourLength(d8, year));
    EXPECT_EQ(33, getHourLength(d9, year));
    EXPECT_EQ(33, getHourLength(d10, year));
    EXPECT_EQ(33, getHourLength(d11, year));
    EXPECT_EQ(33, getHourLength(d12, year));
    EXPECT_EQ(33, getHourLength(d13, year));
}

TEST(getHourLength, worksFor2018)
{
    std::string year = "2018";

    OneDay d1 = OneDay({}, {}, 2);
    OneDay d2 = OneDay({}, {}, 100);
    OneDay d3 = OneDay({}, {}, 200);
    OneDay d4 = OneDay({}, {}, 280);
    OneDay d5 = OneDay({}, {}, 281);
    OneDay d6 = OneDay({}, {}, 282);
    OneDay d7 = OneDay({}, {}, 300);
    OneDay d8 = OneDay({}, {}, 318);
    OneDay d9 = OneDay({}, {}, 319);
    OneDay d10 = OneDay({}, {}, 320);
    OneDay d11 = OneDay({}, {}, 363);
    OneDay d12 = OneDay({}, {}, 365);
    OneDay d13 = OneDay({}, {}, 1);

    EXPECT_EQ(33, getHourLength(d1, year));
    EXPECT_EQ(33, getHourLength(d2, year));
    EXPECT_EQ(33, getHourLength(d3, year));
    EXPECT_EQ(33, getHourLength(d4, year));
    EXPECT_EQ(33, getHourLength(d5, year));
    EXPECT_EQ(33, getHourLength(d6, year));
    EXPECT_EQ(33, getHourLength(d7, year));
    EXPECT_EQ(33, getHourLength(d8, year));
    EXPECT_EQ(33, getHourLength(d9, year));
    EXPECT_EQ(33, getHourLength(d10, year));
    EXPECT_EQ(33, getHourLength(d11, year));
    EXPECT_EQ(33, getHourLength(d12, year));
    EXPECT_EQ(33, getHourLength(d13, year));
}

TEST(getHourLength, worksFor2019)
{
    std::string year = "2019";

    OneDay d1 = OneDay({}, {}, 2);
    OneDay d2 = OneDay({}, {}, 100);
    OneDay d3 = OneDay({}, {}, 200);
    OneDay d4 = OneDay({}, {}, 280);
    OneDay d5 = OneDay({}, {}, 281);
    OneDay d6 = OneDay({}, {}, 282);
    OneDay d7 = OneDay({}, {}, 300);
    OneDay d8 = OneDay({}, {}, 318);
    OneDay d9 = OneDay({}, {}, 319);
    OneDay d10 = OneDay({}, {}, 320);
    OneDay d11 = OneDay({}, {}, 363);
    OneDay d12 = OneDay({}, {}, 365);
    OneDay d13 = OneDay({}, {}, 1);

    EXPECT_EQ(33, getHourLength(d1, year));
    EXPECT_EQ(33, getHourLength(d2, year));
    EXPECT_EQ(33, getHourLength(d3, year));
    EXPECT_EQ(33, getHourLength(d4, year));
    EXPECT_EQ(33, getHourLength(d5, year));
    EXPECT_EQ(33, getHourLength(d6, year));
    EXPECT_EQ(33, getHourLength(d7, year));
    EXPECT_EQ(33, getHourLength(d8, year));
    EXPECT_EQ(33, getHourLength(d9, year));
    EXPECT_EQ(33, getHourLength(d10, year));
    EXPECT_EQ(33, getHourLength(d11, year));
    EXPECT_EQ(33, getHourLength(d12, year));
    EXPECT_EQ(33, getHourLength(d13, year));
}

TEST(getHourLength, worksFor2020)
{
    std::string year = "2020";

    OneDay d1 = OneDay({}, {}, 2);
    OneDay d2 = OneDay({}, {}, 100);
    OneDay d3 = OneDay({}, {}, 200);
    OneDay d4 = OneDay({}, {}, 280);
    OneDay d5 = OneDay({}, {}, 281);
    OneDay d6 = OneDay({}, {}, 282);
    OneDay d7 = OneDay({}, {}, 300);
    OneDay d8 = OneDay({}, {}, 318);
    OneDay d9 = OneDay({}, {}, 319);
    OneDay d10 = OneDay({}, {}, 320);
    OneDay d11 = OneDay({}, {}, 363);
    OneDay d12 = OneDay({}, {}, 365);
    OneDay d13 = OneDay({}, {}, 1);

    EXPECT_EQ(33, getHourLength(d1, year));
    EXPECT_EQ(33, getHourLength(d2, year));
    EXPECT_EQ(33, getHourLength(d3, year));
    EXPECT_EQ(33, getHourLength(d4, year));
    EXPECT_EQ(33, getHourLength(d5, year));
    EXPECT_EQ(33, getHourLength(d6, year));
    EXPECT_EQ(33, getHourLength(d7, year));
    EXPECT_EQ(33, getHourLength(d8, year));
    EXPECT_EQ(33, getHourLength(d9, year));
    EXPECT_EQ(33, getHourLength(d10, year));
    EXPECT_EQ(33, getHourLength(d11, year));
    EXPECT_EQ(33, getHourLength(d12, year));
    EXPECT_EQ(33, getHourLength(d13, year));
}

TEST(getHourLength, worksFor2021)
{
    std::string year = "2021";

    OneDay d1 = OneDay({}, {}, 2);
    OneDay d2 = OneDay({}, {}, 100);
    OneDay d3 = OneDay({}, {}, 200);
    OneDay d4 = OneDay({}, {}, 280);
    OneDay d5 = OneDay({}, {}, 281);
    OneDay d6 = OneDay({}, {}, 282);
    OneDay d7 = OneDay({}, {}, 300);
    OneDay d8 = OneDay({}, {}, 318);
    OneDay d9 = OneDay({}, {}, 319);
    OneDay d10 = OneDay({}, {}, 320);
    OneDay d11 = OneDay({}, {}, 363);
    OneDay d12 = OneDay({}, {}, 365);
    OneDay d13 = OneDay({}, {}, 1);

    EXPECT_EQ(33, getHourLength(d1, year));
    EXPECT_EQ(33, getHourLength(d2, year));
    EXPECT_EQ(33, getHourLength(d3, year));
    EXPECT_EQ(33, getHourLength(d4, year));
    EXPECT_EQ(33, getHourLength(d5, year));
    EXPECT_EQ(33, getHourLength(d6, year));
    EXPECT_EQ(33, getHourLength(d7, year));
    EXPECT_EQ(33, getHourLength(d8, year));
    EXPECT_EQ(33, getHourLength(d9, year));
    EXPECT_EQ(33, getHourLength(d10, year));
    EXPECT_EQ(33, getHourLength(d11, year));
    EXPECT_EQ(33, getHourLength(d12, year));
    EXPECT_EQ(33, getHourLength(d13, year));
}

TEST(getHourLength, worksFor2022)
{
    std::string year = "2022";

    OneDay d1 = OneDay({}, {}, 2);
    OneDay d2 = OneDay({}, {}, 100);
    OneDay d3 = OneDay({}, {}, 200);
    OneDay d4 = OneDay({}, {}, 280);
    OneDay d5 = OneDay({}, {}, 281);
    OneDay d6 = OneDay({}, {}, 282);
    OneDay d7 = OneDay({}, {}, 300);
    OneDay d8 = OneDay({}, {}, 318);
    OneDay d9 = OneDay({}, {}, 319);
    OneDay d10 = OneDay({}, {}, 320);
    OneDay d11 = OneDay({}, {}, 363);
    OneDay d12 = OneDay({}, {}, 365);
    OneDay d13 = OneDay({}, {}, 1);

    EXPECT_EQ(33, getHourLength(d1, year));
    EXPECT_EQ(33, getHourLength(d2, year));
    EXPECT_EQ(33, getHourLength(d3, year));
    EXPECT_EQ(33, getHourLength(d4, year));
    EXPECT_EQ(33, getHourLength(d5, year));
    EXPECT_EQ(33, getHourLength(d6, year));
    EXPECT_EQ(33, getHourLength(d7, year));
    EXPECT_EQ(33, getHourLength(d8, year));
    EXPECT_EQ(33, getHourLength(d9, year));
    EXPECT_EQ(33, getHourLength(d10, year));
    EXPECT_EQ(33, getHourLength(d11, year));
    EXPECT_EQ(33, getHourLength(d12, year));
    EXPECT_EQ(33, getHourLength(d13, year));
}

TEST(getHourLength, worksFor2023)
{
    std::string year = "2023";

    OneDay d1 = OneDay({}, {}, 2);
    OneDay d2 = OneDay({}, {}, 100);
    OneDay d3 = OneDay({}, {}, 200);
    OneDay d4 = OneDay({}, {}, 280);
    OneDay d5 = OneDay({}, {}, 281);
    OneDay d6 = OneDay({}, {}, 282);
    OneDay d7 = OneDay({}, {}, 300);
    OneDay d8 = OneDay({}, {}, 318);
    OneDay d9 = OneDay({}, {}, 319);
    OneDay d10 = OneDay({}, {}, 320);
    OneDay d11 = OneDay({}, {}, 363);
    OneDay d12 = OneDay({}, {}, 365);
    OneDay d13 = OneDay({}, {}, 1);

    EXPECT_EQ(33, getHourLength(d1, year));
    EXPECT_EQ(33, getHourLength(d2, year));
    EXPECT_EQ(33, getHourLength(d3, year));
    EXPECT_EQ(33, getHourLength(d4, year));
    EXPECT_EQ(10, getHourLength(d5, year));
    EXPECT_EQ(10, getHourLength(d6, year));
    EXPECT_EQ(10, getHourLength(d7, year));
    EXPECT_EQ(10, getHourLength(d8, year));
    EXPECT_EQ(10, getHourLength(d9, year));
    EXPECT_EQ(10, getHourLength(d10, year));
    EXPECT_EQ(10, getHourLength(d11, year));
    EXPECT_EQ(10, getHourLength(d12, year));
    EXPECT_EQ(10, getHourLength(d13, year));
}

TEST(getHourLength, worksFor2024)
{
    std::string year = "2024";

    OneDay d1 = OneDay({}, {}, 2);
    OneDay d2 = OneDay({}, {}, 100);
    OneDay d3 = OneDay({}, {}, 200);
    OneDay d4 = OneDay({}, {}, 280);
    OneDay d5 = OneDay({}, {}, 281);
    OneDay d6 = OneDay({}, {}, 282);
    OneDay d7 = OneDay({}, {}, 300);
    OneDay d8 = OneDay({}, {}, 318);
    OneDay d9 = OneDay({}, {}, 319);
    OneDay d10 = OneDay({}, {}, 320);
    OneDay d11 = OneDay({}, {}, 363);
    OneDay d12 = OneDay({}, {}, 365);
    OneDay d13 = OneDay({}, {}, 1);

    EXPECT_EQ(10, getHourLength(d1, year));
    EXPECT_EQ(10, getHourLength(d2, year));
    EXPECT_EQ(10, getHourLength(d3, year));
    EXPECT_EQ(10, getHourLength(d4, year));
    EXPECT_EQ(10, getHourLength(d5, year));
    EXPECT_EQ(10, getHourLength(d6, year));
    EXPECT_EQ(10, getHourLength(d7, year));
    EXPECT_EQ(10, getHourLength(d8, year));
    EXPECT_EQ(10, getHourLength(d9, year));
    EXPECT_EQ(10, getHourLength(d10, year));
    EXPECT_EQ(10, getHourLength(d11, year));
    EXPECT_EQ(10, getHourLength(d12, year));
    EXPECT_EQ(10, getHourLength(d13, year));
}
