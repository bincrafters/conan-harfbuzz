#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
from conans.tools import SystemPackageTool
import os


class HarfbuzzConan(ConanFile):
    name = "harfbuzz"
    version = "1.7.6"
    description = "HarfBuzz is an OpenType text shaping engine."
    homepage = "http://harfbuzz.org"
    url = "http://github.com/bincrafters/conan-harfbuzz"
    license = "MIT"
    author = "Bincrafters <bincrafters@gmail.com>"
    settings = "os", "arch", "compiler", "build_type"
    generators = "cmake"
    short_paths = True
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "with_freetype": [True, False],
        "with_icu": [True, False],
        "with_glib": [True, False],
        "with_graphite2": [True, False]
    }
    default_options = ("shared=False", "fPIC=True", "with_freetype=False",
                       "with_icu=False", "with_glib=False", "with_graphite2=False")
    exports_sources = ("CMakeLists.txt", "cmake.patch")
    exports = "FindHarfbuzz.cmake"
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"

    def build_requirements(self):
        if tools.OSInfo().is_linux:
            installer = SystemPackageTool()
            installer.install("ragel")

    def requirements(self):
        if self.options.with_freetype:
            self.build_requires("freetype/2.8.1@bincrafters/stable")

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        source_url = "https://github.com/harfbuzz/harfbuzz"
        tools.get("{0}/archive/{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self.source_subfolder)
        tools.patch(base_path=self.source_subfolder, patch_file="cmake.patch")

    def configure_cmake_compiler_flags(self, cmake):
        flags = []
        compiler = str(self.settings.compiler)
        if compiler in ("clang", "apple-clang"):
            flags.append("-Wno-deprecated-declarations")
        cmake.definitions["CMAKE_C_FLAGS"] = " ".join(flags)
        cmake.definitions["CMAKE_CXX_FLAGS"] = cmake.definitions["CMAKE_C_FLAGS"]
        return cmake

    def configure_cmake_macos(self, cmake):
        if str(self.settings.os) in ["Macos", "iOS", "watchOS", "tvOS"]:
            cmake.definitions["CMAKE_MACOSX_RPATH"] = True
        return cmake

    def configure_cmake(self):
        cmake = CMake(self)
        cmake = self.configure_cmake_compiler_flags(cmake)
        cmake = self.configure_cmake_macos(cmake)
        if self.settings.os != "Windows":
            cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = self.options.fPIC
        cmake.definitions["HB_HAVE_FREETYPE"] = self.options.with_freetype
        cmake.definitions["HB_HAVE_ICU"] = self.options.with_icu
        cmake.definitions["HB_HAVE_GLIB"] = self.options.with_glib
        cmake.definitions["HB_HAVE_GRAPHITE2"] = self.options.with_graphite2
        cmake.configure(build_folder=self.build_subfolder)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        self.copy("FindHarfbuzz.cmake", dst="res")
        self.copy("COPYING", dst="licenses", keep_path=False)
        cmake = self.configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("m")
        if self.settings.compiler == 'Visual Studio' and not self.options.shared:
            self.cpp_info.libs.extend(["dwrite", "rpcrt4", "usp10"])
