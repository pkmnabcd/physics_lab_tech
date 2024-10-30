#include <cstdlib>
#include <iostream>
#include <filesystem>

// Complile with command:
// g++ monthlyCleaner.cpp -o MonthlyCleaner -std=c++20 -Wall -Wextra -pedantic
int main()
{
    const std::filesystem::path currentDir = std::filesystem::current_path();
    std::cout << currentDir.string() << std::endl;

    for (auto const& dir_entry : std::filesystem::directory_iterator{currentDir})
    {
         std::cout << dir_entry.path().string() << std::endl;
    }
}
