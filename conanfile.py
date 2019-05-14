# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class HarfbuzzConan(ConanFile):
    name = "harfbuzz"
    version = "2.3.0"
    description = "HarfBuzz is an OpenType text shaping engine."
    homepage = "https://github.com/harfbuzz/harfbuzz"
    url = "http://github.com/bincrafters/conan-harfbuzz"
    license = "MIT"
    author = "Bincrafters <bincrafters@gmail.com>"
    settings = "os", "arch", "compiler", "build_type"
    generators = "cmake"
    topics = ("conan", "harfbuzz", "text", "open-type", "text-engine")
    short_paths = True
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "with_freetype": [True, False]
    }
    default_options = {'shared': False, 'fPIC': True, 'with_freetype': False}
    exports = ["FindHarfBuzz.cmake", "LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def build_requirements(self):
        if self.settings.os == "Linux" and not tools.which("ragel"):
            self.build_requires.add("ragel_installer/6.10@bincrafters/stable")

    def requirements(self):
        if self.options.with_freetype:
            self.requires.add("freetype/2.9.0@bincrafters/stable")

    def configure(self):
        del self.settings.compiler.libcxx

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        sha256 = "4d6b73c4bbcf1f986ab63fb9fed853ef725698d7f1e85bc389efca2640ddb135"
        tools.get("{0}/archive/{1}.tar.gz".format(self.homepage, self.version), sha256=sha256)
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake_compiler_flags(self, cmake):
        flags = []
        compiler = str(self.settings.compiler)
        if compiler in ("clang", "apple-clang"):
            flags.append("-Wno-deprecated-declarations")
        cmake.definitions["CMAKE_C_FLAGS"] = " ".join(flags)
        cmake.definitions["CMAKE_CXX_FLAGS"] = cmake.definitions["CMAKE_C_FLAGS"]
        return cmake

    def _configure_cmake_macos(self, cmake):
        if str(self.settings.os) in ["Macos", "iOS", "watchOS", "tvOS"]:
            cmake.definitions["CMAKE_MACOSX_RPATH"] = True
        return cmake

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake = self._configure_cmake_compiler_flags(cmake)
        cmake = self._configure_cmake_macos(cmake)
        cmake.definitions["HB_HAVE_FREETYPE"] = self.options.with_freetype
        cmake.definitions["HB_BUILD_TESTS"] = False
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy("FindHarfBuzz.cmake")
        self.copy("COPYING", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("m")
        if self.settings.compiler == 'Visual Studio' and not self.options.shared:
            self.cpp_info.libs.extend(["dwrite", "rpcrt4", "usp10"])
        if self.settings.os in ["Macos", "iOS", "watchOS", "tvOS"]:
            self.cpp_info.exelinkflags.extend(["-framework CoreFoundation", "-framework CoreGraphics", "-framework CoreText"])
            self.cpp_info.sharedlinkflags = self.cpp_info.exelinkflags
