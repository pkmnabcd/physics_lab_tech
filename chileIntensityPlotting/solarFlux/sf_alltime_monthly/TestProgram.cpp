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
