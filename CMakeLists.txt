project(cmake_wrapper)

set(CMAKE_VERBOSE_MAKEFILE TRUE)

include(conanbuildinfo.cmake)
conan_basic_setup()

add_subdirectory(source_subfolder)
