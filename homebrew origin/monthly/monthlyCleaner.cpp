#include <cstdlib>
#include <iostream>
#include <filesystem>
#include <regex>

// Complile with command:
// g++ monthlyCleaner.cpp -o MonthlyCleaner -std=c++20 -Wall -Wextra -pedantic
int main()
{
    const std::filesystem::path currentDir = std::filesystem::current_path();
    const std::string pattern_text = "OH_Andover_ALO[0-9][0-9]day[0-9]{1,3}.dat";
    auto regexpr = std::regex(pattern_text);

    for (auto const& dir_entry : std::filesystem::directory_iterator{currentDir})
    {
        const std::string filename = dir_entry.path().filename().string();
        if (std::regex_match(filename.begin(), filename.end(), regexpr))
        {
            std::cout << "Filename match: " << filename << std::endl;
            #ifdef _WIN32
                std::string command = ".\\chileTempCleanerAndGrapher.bat ";
            #else
                std::string command = "./chileTempCleanerAndGrapher.sh ";
            #endif
            command += filename;
            std::cout << "Command: " << command << std::endl;
            std::system(command.c_str());
        }
    }
}
