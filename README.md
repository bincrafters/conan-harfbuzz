[![Build Status](https://travis-ci.org/bincrafters/conan-harfbuzz.svg)](https://travis-ci.org/bincrafters/conan-harfbuzz)


# conan-harfbuzz

[Conan.io](https://conan.io) package for H[arfbuzz library](http://harfbuzz.org).

The packages generated with this **conanfile** can be found in [conan.io](https://conan.io/source/harfbuzz/1.7.1/bincrafters/stable).

## Build packages

Download conan client from [Conan.io](https://conan.io) and run:

    $ python build.py

## Upload packages to server

    $ conan upload harfbuzz/1.7.1@bincrafters/stable --all
    
## Reuse the packages

### Basic setup

    $ conan install harfbuzz/1.7.1@bincrafters/stable
    
### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*
    
    [requires]
    harfbuzz/1.7.1@bincrafters/stable

    [options]
    harfbuzz:shared=true # false
    
    [generators]
    txt
    cmake

Complete the installation of requirements for your project running:</small></span>

    conan install .

Project setup installs the library (and all his dependencies) and generates the files *conanbuildinfo.txt* and *conanbuildinfo.cmake* with all the paths and variables that you need to link with your dependencies.
