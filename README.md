[![Build Status](https://travis-ci.org/lasote/conan-harfbuzz.svg)](https://travis-ci.org/lasote/conan-harfbuzz)


# conan-harfbuzz

[Conan.io](https://conan.io) package for harfbuzz library

The packages generated with this **conanfile** can be found in [conan.io](https://conan.io/source/harfbuzz/1.2.4/lasote/stable).

## Build packages

Download conan client from [Conan.io](https://conan.io) and run:

    $ python build.py

## Upload packages to server

    $ conan upload harfbuzz/2.0.3@lasote/stable --all
    
## Reuse the packages

### Basic setup

    $ conan install harfbuzz/2.0.3@lasote/stable
    
### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*
    
    [requires]
    harfbuzz/2.0.3@lasote/stable

    [options]
    harfbuzz:shared=true # false
    
    [generators]
    txt
    cmake

Complete the installation of requirements for your project running:</small></span>

    conan install .

Project setup installs the library (and all his dependencies) and generates the files *conanbuildinfo.txt* and *conanbuildinfo.cmake* with all the paths and variables that you need to link with your dependencies.
