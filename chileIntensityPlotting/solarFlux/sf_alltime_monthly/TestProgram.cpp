#include "OneYear.hpp"
#include "parsing.hpp"

#include <gtest/gtest.h>
#include <string>
#include <vector>

int main(int argc, char* argv[])
{
    testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}

TEST(split, handlesNoChPresent)
{
    auto result = split("hehkl;ea", ',');
    EXPECT_EQ(1, result.size());
    EXPECT_EQ("hehkl;ea", result[0]);
}

TEST(split, handlesChAtStartAndEnd)
{
    auto result = split(",hehkl;ea,", ',');
    EXPECT_EQ(1, result.size());
    EXPECT_EQ("hehkl;ea", result[0]);

    result = split(",5839,103.53,776", ',');
    EXPECT_EQ(3, result.size());
    EXPECT_EQ("5839", result[0]);
    EXPECT_EQ("103.53", result[1]);
    EXPECT_EQ("776", result[2]);

    result = split("5839,103.53,776,", ',');
    EXPECT_EQ(3, result.size());
    EXPECT_EQ("5839", result[0]);
    EXPECT_EQ("103.53", result[1]);
    EXPECT_EQ("776", result[2]);

    result = split(",5839,103.53,776,", ',');
    EXPECT_EQ(3, result.size());
    EXPECT_EQ("5839", result[0]);
    EXPECT_EQ("103.53", result[1]);
    EXPECT_EQ("776", result[2]);
}

TEST(split, handlesNormal)
{
    auto result = split("gh,krla,feja,fe", ',');
    EXPECT_EQ(4, result.size());
    EXPECT_EQ("gh", result[0]);
    EXPECT_EQ("krla", result[1]);
    EXPECT_EQ("feja", result[2]);
    EXPECT_EQ("fe", result[3]);

    result = split("gh,krla,feja,fe\n", ',');
    EXPECT_EQ(4, result.size());
    EXPECT_EQ("gh", result[0]);
    EXPECT_EQ("krla", result[1]);
    EXPECT_EQ("feja", result[2]);
    EXPECT_EQ("fe\n", result[3]);

    result = split("5839,103.53,776", ',');
    EXPECT_EQ(3, result.size());
    EXPECT_EQ("5839", result[0]);
    EXPECT_EQ("103.53", result[1]);
    EXPECT_EQ("776", result[2]);
}

TEST(montlyAveragesOneMonth, worksWhenSfOHSame)
{
    auto y1 = OneYear("2024",
                      { 4.2, 3.1, 6.5 },
                      { 5.2, 1.1, 0.6 },
                      { 1, 1, 1 },
                      { 1, 1, 1 });

    EXPECT_FLOAT_EQ(4.6, y1.getOHAverage()[0]);
    EXPECT_NEAR(1.734935, y1.getOHStdDev()[0], 0.0001);
    EXPECT_FLOAT_EQ(2.3, y1.getSfAverage()[0]);
    EXPECT_NEAR(2.523886, y1.getSfStdDev()[0], 0.0001);

    EXPECT_EQ(1, y1.getOHAverage().size());
    EXPECT_EQ(1, y1.getOHStdDev().size());
    EXPECT_EQ(1, y1.getSfAverage().size());
    EXPECT_EQ(1, y1.getSfStdDev().size());

    EXPECT_EQ(1, y1.getCollapsedOHMonths().size());
    EXPECT_EQ(1, y1.getCollapsedSfMonths().size());
    EXPECT_EQ(1, y1.getCollapsedOHMonths()[0]);
    EXPECT_EQ(1, y1.getCollapsedSfMonths()[0]);
}

TEST(montlyAveragesOneMonth, worksWhenSfOHDifferent)
{
    auto y1 = OneYear("2024",
                      { 4.2, 3.1, 6.5 },
                      { 5.2, 1.1, 0.6 },
                      { 1, 1, 1 },
                      { 12, 12, 12 });

    EXPECT_FLOAT_EQ(4.6, y1.getOHAverage()[0]);
    EXPECT_NEAR(1.734935, y1.getOHStdDev()[0], 0.0001);
    EXPECT_FLOAT_EQ(2.3, y1.getSfAverage()[0]);
    EXPECT_NEAR(2.523886, y1.getSfStdDev()[0], 0.0001);

    EXPECT_EQ(1, y1.getOHAverage().size());
    EXPECT_EQ(1, y1.getOHStdDev().size());
    EXPECT_EQ(1, y1.getSfAverage().size());
    EXPECT_EQ(1, y1.getSfStdDev().size());

    EXPECT_EQ(1, y1.getCollapsedOHMonths().size());
    EXPECT_EQ(1, y1.getCollapsedSfMonths().size());
    EXPECT_EQ(1, y1.getCollapsedOHMonths()[0]);
    EXPECT_EQ(12, y1.getCollapsedSfMonths()[0]);

    auto y2 = OneYear("2024",
                      { 4.2, 3.1, 6.5 },
                      { 5.2, 1.1, 0.6, 5.2, 1.1, 0.6 },
                      { 1, 1, 1 },
                      { 10, 10, 10, 10, 10, 10 });

    EXPECT_FLOAT_EQ(4.6, y2.getOHAverage()[0]);
    EXPECT_NEAR(1.734935, y2.getOHStdDev()[0], 0.0001);
    EXPECT_FLOAT_EQ(2.3, y2.getSfAverage()[0]);
    EXPECT_NEAR(2.257432, y2.getSfStdDev()[0], 0.0001);

    EXPECT_EQ(1, y2.getOHAverage().size());
    EXPECT_EQ(1, y2.getOHStdDev().size());
    EXPECT_EQ(1, y2.getSfAverage().size());
    EXPECT_EQ(1, y2.getSfStdDev().size());

    EXPECT_EQ(1, y2.getCollapsedOHMonths().size());
    EXPECT_EQ(1, y2.getCollapsedSfMonths().size());
    EXPECT_EQ(1, y2.getCollapsedOHMonths()[0]);
    EXPECT_EQ(10, y2.getCollapsedSfMonths()[0]);
}

TEST(montlyAveragesMultipleMonth, worksWhenSfOHSame)
{
    auto y1 = OneYear("2024",
                      { 4.2, 3.1, 6.5, 1.5, 4.5, 6.4, 3.6 },
                      { 5.2, 1.1, 0.6, 2.0, 4.0, 1.5, 0.5 },
                      { 1, 1, 1, 2, 2, 12, 12 },
                      { 1, 1, 1, 2, 2, 12, 12 });

    EXPECT_FLOAT_EQ(4.6, y1.getOHAverage()[0]);
    EXPECT_FLOAT_EQ(3.0, y1.getOHAverage()[1]);
    EXPECT_FLOAT_EQ(5.0, y1.getOHAverage()[2]);
    EXPECT_FLOAT_EQ(2.3, y1.getSfAverage()[0]);
    EXPECT_FLOAT_EQ(3.0, y1.getSfAverage()[1]);
    EXPECT_FLOAT_EQ(1.0, y1.getSfAverage()[2]);

    EXPECT_NEAR(1.734935, y1.getOHStdDev()[0], 0.0001);
    EXPECT_NEAR(2.121320, y1.getOHStdDev()[1], 0.0001);
    EXPECT_NEAR(1.979899, y1.getOHStdDev()[2], 0.0001);
    EXPECT_NEAR(2.523886, y1.getSfStdDev()[0], 0.0001);
    EXPECT_NEAR(1.414214, y1.getSfStdDev()[1], 0.0001);
    EXPECT_NEAR(0.707107, y1.getSfStdDev()[2], 0.0001);

    EXPECT_EQ(3, y1.getOHAverage().size());
    EXPECT_EQ(3, y1.getOHStdDev().size());
    EXPECT_EQ(3, y1.getSfAverage().size());
    EXPECT_EQ(3, y1.getSfStdDev().size());

    EXPECT_EQ(3, y1.getCollapsedOHMonths().size());
    EXPECT_EQ(3, y1.getCollapsedSfMonths().size());

    EXPECT_EQ(1, y1.getCollapsedOHMonths()[0]);
    EXPECT_EQ(2, y1.getCollapsedOHMonths()[1]);
    EXPECT_EQ(12, y1.getCollapsedOHMonths()[2]);
    EXPECT_EQ(1, y1.getCollapsedSfMonths()[0]);
    EXPECT_EQ(2, y1.getCollapsedSfMonths()[1]);
    EXPECT_EQ(12, y1.getCollapsedSfMonths()[2]);
}

TEST(montlyAveragesMultipleMonth, worksWhenSfOHDifferent)
{
    auto y1 = OneYear("2024",
                      { 4.2, 3.1, 6.5, 1.5, 4.5, 6.4, 3.6 },
                      { 5.2, 1.1, 0.6, 2.0, 4.0, 1.5, 0.5 },
                      { 1, 1, 1, 2, 2, 12, 12 },
                      { 2, 2, 2, 3, 3, 11, 11 });

    EXPECT_FLOAT_EQ(4.6, y1.getOHAverage()[0]);
    EXPECT_FLOAT_EQ(3.0, y1.getOHAverage()[1]);
    EXPECT_FLOAT_EQ(5.0, y1.getOHAverage()[2]);
    EXPECT_FLOAT_EQ(2.3, y1.getSfAverage()[0]);
    EXPECT_FLOAT_EQ(3.0, y1.getSfAverage()[1]);
    EXPECT_FLOAT_EQ(1.0, y1.getSfAverage()[2]);

    EXPECT_NEAR(1.734935, y1.getOHStdDev()[0], 0.0001);
    EXPECT_NEAR(2.121320, y1.getOHStdDev()[1], 0.0001);
    EXPECT_NEAR(1.979899, y1.getOHStdDev()[2], 0.0001);
    EXPECT_NEAR(2.523886, y1.getSfStdDev()[0], 0.0001);
    EXPECT_NEAR(1.414214, y1.getSfStdDev()[1], 0.0001);
    EXPECT_NEAR(0.707107, y1.getSfStdDev()[2], 0.0001);

    EXPECT_EQ(3, y1.getOHAverage().size());
    EXPECT_EQ(3, y1.getOHStdDev().size());
    EXPECT_EQ(3, y1.getSfAverage().size());
    EXPECT_EQ(3, y1.getSfStdDev().size());

    EXPECT_EQ(3, y1.getCollapsedOHMonths().size());
    EXPECT_EQ(3, y1.getCollapsedSfMonths().size());

    EXPECT_EQ(1, y1.getCollapsedOHMonths()[0]);
    EXPECT_EQ(2, y1.getCollapsedOHMonths()[1]);
    EXPECT_EQ(12, y1.getCollapsedOHMonths()[2]);
    EXPECT_EQ(2, y1.getCollapsedSfMonths()[0]);
    EXPECT_EQ(3, y1.getCollapsedSfMonths()[1]);
    EXPECT_EQ(11, y1.getCollapsedSfMonths()[2]);

    auto y2 = OneYear("2024",
                      { 4.2, 3.1, 6.5, 1.5, 4.5, 6.4, 3.6 },
                      { 5.2, 1.1, 0.6, 2.0, 4.0, 1.5, 0.5, 1.0 },
                      { 1, 1, 1, 2, 2, 12, 12 },
                      { 1, 1, 1, 2, 2, 12, 12, 12 });

    EXPECT_FLOAT_EQ(4.6, y2.getOHAverage()[0]);
    EXPECT_FLOAT_EQ(3.0, y2.getOHAverage()[1]);
    EXPECT_FLOAT_EQ(5.0, y2.getOHAverage()[2]);
    EXPECT_FLOAT_EQ(2.3, y2.getSfAverage()[0]);
    EXPECT_FLOAT_EQ(3.0, y2.getSfAverage()[1]);
    EXPECT_FLOAT_EQ(1.0, y2.getSfAverage()[2]);

    EXPECT_NEAR(1.734935, y2.getOHStdDev()[0], 0.0001);
    EXPECT_NEAR(2.121320, y2.getOHStdDev()[1], 0.0001);
    EXPECT_NEAR(1.979899, y2.getOHStdDev()[2], 0.0001);
    EXPECT_NEAR(2.523886, y2.getSfStdDev()[0], 0.0001);
    EXPECT_NEAR(1.414214, y2.getSfStdDev()[1], 0.0001);
    EXPECT_NEAR(0.500000, y2.getSfStdDev()[2], 0.0001);

    EXPECT_EQ(3, y2.getOHAverage().size());
    EXPECT_EQ(3, y2.getOHStdDev().size());
    EXPECT_EQ(3, y2.getSfAverage().size());
    EXPECT_EQ(3, y2.getSfStdDev().size());

    EXPECT_EQ(3, y2.getCollapsedOHMonths().size());
    EXPECT_EQ(3, y2.getCollapsedSfMonths().size());

    EXPECT_EQ(1, y2.getCollapsedOHMonths()[0]);
    EXPECT_EQ(2, y2.getCollapsedOHMonths()[1]);
    EXPECT_EQ(12, y2.getCollapsedOHMonths()[2]);
    EXPECT_EQ(1, y2.getCollapsedSfMonths()[0]);
    EXPECT_EQ(2, y2.getCollapsedSfMonths()[1]);
    EXPECT_EQ(12, y2.getCollapsedSfMonths()[2]);
}
