cmake_minimum_required(VERSION 3.16)

project(Prototyping C CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

if(UNIX)
    set(CMAKE_INSTALL_RPATH "$ORIGIN")
    set(CMAKE_BUILD_WITH_INSTALL_RPATH TRUE)
elseif(WIN32)
    add_compile_definitions(
        WINVER=0x0601
        _WIN32_WINNT=0x0601
        NOMINMAX
    )
    add_compile_options(/utf-8 /permissive-)
endif()

find_package(spdlog REQUIRED CONFIG)
find_package(expected-lite REQUIRED CONFIG)
find_package(Catch2 REQUIRED CONFIG)
find_package(Boost REQUIRED CONFIG)
find_package(range-v3 REQUIRED CONFIG)
find_package(Iconv REQUIRED CONFIG)
find_package(nlohmann-json REQUIRED CONFIG)
find_package(uWebSockets REQUIRED CONFIG)
find_package(concurrent-queue REQUIRED CONFIG)
find_package(threadpool REQUIRED CONFIG)

include_directories(src)
add_subdirectory(src)
