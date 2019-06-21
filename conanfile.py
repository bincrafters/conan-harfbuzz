# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class HarfbuzzConan(ConanFile):
    name = "harfbuzz"
    version = "2.4.0"
    description = "HarfBuzz is an OpenType text shaping engine."
    topics = ("conan", "harfbuzz", "opentype", "text", "engine")
    url = "http://github.com/bincrafters/conan-harfbuzz"
    homepage = "http://harfbuzz.org"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "MIT"
    exports = ["FindHarfBuzz.cmake", "LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    short_paths = True

    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "with_freetype": [True, False],
        "with_icu": [True, False]
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "with_freetype": True,
        "with_icu": False
    }

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def requirements(self):
        if self.options.with_freetype:
            self.requires.add("freetype/2.9.1@bincrafters/stable")
        if self.options.with_icu:
            self.requires.add("icu/63.1@bincrafters/stable")

    def configure(self):
        del self.settings.compiler.libcxx

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        source_url = "https://github.com/harfbuzz/harfbuzz"
        sha256 = "dc3132a479c8c4fa1c9dd09d433a3ab9b0d2f302f844a764d57faf1629bfb9c5"
        tools.get("{0}/archive/{1}.tar.gz".format(source_url, self.version), sha256=sha256)
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

        if self.version == "2.4.0":
            tools.replace_in_file("source_subfolder/src/hb-coretext.cc",
                "bool backward = HB_DIRECTION_IS_BACKWARD (buffer->props.direction);",
                "HB_UNUSED bool backward = HB_DIRECTION_IS_BACKWARD (buffer->props.direction);")

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
        cmake.definitions["HB_HAVE_ICU"] = self.options.with_icu

        if self.options.with_icu:
            cmake.definitions["CMAKE_CXX_STANDARD"] = "17"

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
        self.cpp_info.includedirs.append(os.path.join("include", "harfbuzz"))
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("m")
        if self.settings.compiler == 'Visual Studio' and not self.options.shared:
            self.cpp_info.libs.extend(["dwrite", "rpcrt4", "usp10"])
        if self.settings.os in ["Macos", "iOS", "watchOS", "tvOS"]:
            self.cpp_info.exelinkflags.extend(["-framework CoreFoundation", "-framework CoreGraphics", "-framework CoreText"])
            self.cpp_info.sharedlinkflags = self.cpp_info.exelinkflags
