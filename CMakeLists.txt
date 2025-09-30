cmake_minimum_required(VERSION 3.16)
project(VNNLibPython LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

if(NOT EXISTS "${CMAKE_SOURCE_DIR}/cpp/.git")
    message(FATAL_ERROR "Submodule 'cpp' is missing. Run: git submodule update --init --recursive")
endif()

add_subdirectory(cpp)

set(PYBIND11_FINDPYTHON ON)
find_package(pybind11 REQUIRED)

pybind11_add_module(_core vnnlib/_core.cpp)
target_link_libraries(_core PRIVATE VNNLib)

target_include_directories(_core
    PRIVATE
        ${CMAKE_SOURCE_DIR}/cpp/include
        ${CMAKE_SOURCE_DIR}/cpp/include/util
        ${CMAKE_SOURCE_DIR}/cpp/src/generated
)

set_target_properties(_core PROPERTIES
    INSTALL_RPATH "$ORIGIN"
)

install(TARGETS _core VNNLib
    LIBRARY DESTINATION vnnlib   # .so
    ARCHIVE DESTINATION vnnlib   # .a
    RUNTIME DESTINATION vnnlib   # .dll
)


