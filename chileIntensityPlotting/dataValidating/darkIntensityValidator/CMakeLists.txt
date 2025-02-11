cmake_minimum_required(VERSION 3.14)

set(PROJECT_NAME DarkIntensityValidator)
project(${PROJECT_NAME})

#
# Manually specifying all the source files.
#
set(HEADER_FILES
    strTool.hpp
    OneDay.hpp
    parsing.hpp
)

set(SOURCE_FILES
    strTool.cpp
    OneDay.cpp
    parsing.cpp
)

#
# This is the main target
#
add_executable(${PROJECT_NAME} ${HEADER_FILES} ${SOURCE_FILES} main.cpp)

#
# We want the C++ 20 standard for our project
#
set_property(TARGET ${PROJECT_NAME} PROPERTY CXX_STANDARD 23)

if (CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
    target_compile_options(${PROJECT_NAME} PRIVATE /W4 /permissive-)
elseif (CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
    target_compile_options(${PROJECT_NAME} PRIVATE -Wall -Wextra -pedantic )
endif()

#
# Prepare a pre-build step to run clang-format over all the [ch]pp source files.
# Start by finding the location of the clang-format executable.
#
find_program(CLANG_FORMAT "clang-format")
if (CLANG_FORMAT)
    #
    # Need to take the simple source file locations used for the project and get their full
    # file system locations for use in putting together the clang-format command line
    #
    unset(SOURCE_FILES_PATHS)
    foreach(SOURCE_FILE ${HEADER_FILES} ${SOURCE_FILES} ${UNIT_TEST_FILES} main.cpp)
        get_source_file_property(WHERE ${SOURCE_FILE} LOCATION)
        set(SOURCE_FILES_PATHS ${SOURCE_FILES_PATHS} ${WHERE})
    endforeach()

    #
    # This creates the clang-format target/command
    #
    add_custom_target(
        ClangFormat
        COMMAND ${CLANG_FORMAT}
        -i
        -style=file
        ${SOURCE_FILES_PATHS}
    )
    #
    # This makes the clang-format target a dependency of the main project
    #
    add_dependencies(${PROJECT_NAME} ClangFormat)
else()
    message("Unable to find clang-format")
endif()
