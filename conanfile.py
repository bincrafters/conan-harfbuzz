#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
from conans.tools import SystemPackageTool
import os

class HarfbuzzConan(ConanFile):
    name = "harfbuzz"
    version = "1.7.1"
    homepage = "http://harfbuzz.org"
    description="HarfBuzz is an OpenType text shaping engine."

    url="http://github.com/bincrafters/conan-harfbuzz"
    license="MIT"

    settings = "os", "arch", "compiler", "build_type"
    short_paths = True
    generators = "cmake"

    options = {"shared": [True, False],
               "fPIC": [True, False],
               "with_freetype": [True, False]}

    default_options = "shared=False", \
                      "fPIC=True", \
                      "with_freetype=False"

    exports_sources = "CMakeLists.txt"
    exports = "FindHarfbuzz.cmake"

    source_url="https://github.com/behdad/harfbuzz/archive/%s.tar.gz" % version

    def build_requirements(self):
        if self.settings.os == "Windows":
            self.build_requires("ragel_installer/6.10@sigmoidal/stable")
        else:
            pack_name = None
            if os_info.is_linux:
                pack_name = "ragel"

            if pack_name:
                installer = SystemPackageTool()
                installer.install(pack_name)

        if self.options.with_freetype:
            self.build_requires("freetype/2.8.1@bincrafters/testing")


    def source(self):
        tools.get(self.source_url)
        os.rename('{name}-{version}'.format(name=self.name, version=self.version),
                  'sources')

    def build(self):
        cmake = CMake(self)
        
        if str(self.settings.os) in ["Macos", "iOS", "watchOS", "tvOS"]:
            cmake.definitions["CMAKE_MACOSX_RPATH"] = "On"

        flags = []
        
        compiler = str(self.settings.compiler)

        if compiler in ("clang", "apple-clang"):
            # without the following, compilation gets stuck indefinitely
            flags.append("-Wno-deprecated-declarations")
               
        cmake.definitions["CMAKE_C_FLAGS"] = " ".join(flags)
        cmake.definitions["CMAKE_CXX_FLAGS"] = cmake.definitions["CMAKE_C_FLAGS"]
        
        cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = self.options.fPIC
 
        cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared

        cmake.definitions["HB_HAVE_FREETYPE"] = self.options.with_freetype

        os_info = tools.OSInfo()

        # UniScribe was replaced by DirectWrite after Windows 7 (although still maintained)
        if os_info.is_windows == "Windows":
            if os_info.os_version >= "7":
                cmake.definitions["HB_HAVE_DIRECTWRITE"] = "On"
            else:
                cmake.definitions["HB_HAVE_UNISCRIBE"] = "On"
        # todo
        #cmake.definitions["HB_HAVE_ICU"] = "On"

        cmake.configure(source_dir="..", build_dir="build")
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("FindHarfbuzz.cmake", ".", ".")
        self.copy("COPYING", dst="licenses", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["harfbuzz"]

        os_info = tools.OSInfo()
        if self.settings.os == "Windows" and not self.options.shared:
            if os_info.os_version >= "7":
                self.cpp_info.libs.append("dwrite")
                self.cpp_info.libs.append("rpcrt4")
            else:
                self.cpp_info.libs.append("usp10")


                
