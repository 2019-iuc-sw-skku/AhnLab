cmake_minimum_required(VERSION 3.14)
project(Ahnreport)

set(CMAKE_CXX_STANDARD 14)
SET ( CMAKE_VERBOSE_MAKEFILE true )

add_executable(Ahnreport main.cpp input/manage_input.cpp input/manage_input.h)