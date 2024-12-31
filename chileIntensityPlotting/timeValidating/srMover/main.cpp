#include <cstdlib>
#include <filesystem>
#include <format>
#include <print>
#include <regex>
#include <string>
#include <vector>

bool isSrImage(std::string filename)
{
    std::vector<std::string> patterns = {
        "866A_sr[0-9]{4}.tif",
        "868A_sr[0-9]{4}.tif",
        "BG_sr[0-9]{4}.tif",
        "Dark_sr[0-9]{4}.tif",
        "P12A_sr[0-9]{4}.tif",
        "P14A_sr[0-9]{4}.tif"
    };
    for (std::string& pattern : patterns)
    {
        auto regexpr = std::regex(pattern);
        if (std::regex_match(filename.begin(), filename.end(), regexpr))
        {
            return true;
        }
    }

    return false;
}

int main()
{
    std::filesystem::path currentDir = std::filesystem::current_path();
    auto dirEntries = std::filesystem::directory_iterator(currentDir);
    std::filesystem::create_directory(currentDir / "sr_data");

    for (auto& dir_entry : dirEntries)
    {
        std::filesystem::path path = dir_entry.path();
        std::string filename = path.filename().string();
        std::print("{}\n", filename);
        bool isSr = isSrImage(filename);
        std::print("\tIs sr? {}.\n", isSr);

        if (isSr)
        {
            std::string command = std::format("mv {0} sr_data/{0}", filename);
            std::print("Running the command: {}\n", command);
            std::system(command.c_str());
        }
    }

    return 0;
}
