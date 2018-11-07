#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class HarfbuzzConan(ConanFile):
    name = "harfbuzz"
    version = "1.7.2"
    homepage = "http://harfbuzz.org"
    description = "HarfBuzz is an OpenType text shaping engine."

    url = "http://github.com/bincrafters/conan-harfbuzz"
    license = "MIT"

    settings = "os", "arch", "compiler", "build_type"
    generators = "cmake"
    short_paths = True

    options = {"shared": [True, False],
               "fPIC": [True, False],
               "with_freetype": [True, False],
               "with_icu": [True, False]}

    default_options = {'shared': False, 'fPIC': True, 'with_freetype': False, 'with_icu': False}

    exports_sources = "CMakeLists.txt"
    exports = "FindHarfbuzz.cmake"

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def build_requirements(self):
        self.build_requires("ragel_installer/6.10@bincrafters/stable")

        if self.options.with_freetype:
            self.build_requires("freetype/2.8.1@bincrafters/stable")

        if self.options.with_icu:
            self.build_requires("icu/60.1@bincrafters/stable")

    def source(self):
        tools.get("https://github.com/behdad/harfbuzz/archive/%s.tar.gz" % self.version)
        os.rename('{name}-{version}'.format(name=self.name, version=self.version), self._source_subfolder)

    def _configure_cmake(self):
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

        cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared

        cmake.definitions["HB_HAVE_FREETYPE"] = self.options.with_freetype

        os_info = tools.OSInfo()

        # UniScribe was replaced by DirectWrite after Windows 7 (although still maintained)
        if os_info.is_windows == "Windows":
            if os_info.os_version >= "7":
                cmake.definitions["HB_HAVE_DIRECTWRITE"] = "On"
            else:
                cmake.definitions["HB_HAVE_UNISCRIBE"] = "On"

        cmake.definitions["HB_HAVE_ICU"] = self.options.with_icu

        cmake.configure(source_dir="..", build_dir=self._build_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
        self.copy("FindHarfbuzz.cmake", ".", ".")
        self.copy("COPYING", src=self._source_subfolder, dst="licenses", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["harfbuzz"]

        os_info = tools.OSInfo()
        if self.settings.os == "Windows" and not self.options.shared:
            if os_info.os_version >= "7":
                self.cpp_info.libs.append("dwrite")
                self.cpp_info.libs.append("rpcrt4")
            else:
                self.cpp_info.libs.append("usp10")
