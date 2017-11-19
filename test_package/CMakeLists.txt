project(test_package CXX)
cmake_minimum_required(VERSION 2.8.12)

set(CMAKE_VERBOSE_MAKEFILE TRUE)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

if (APPLE)
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -framework CoreFoundation")
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -framework CoreGraphics")
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -framework CoreText")
endif()

file(GLOB SOURCE_FILES *.cpp)

add_executable(${CMAKE_PROJECT_NAME} ${SOURCE_FILES})
target_link_libraries(${CMAKE_PROJECT_NAME} ${CONAN_LIBS})
set_property(TARGET ${CMAKE_PROJECT_NAME} PROPERTY CXX_STANDARD 11)