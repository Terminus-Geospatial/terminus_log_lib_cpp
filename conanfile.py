#**************************** INTELLECTUAL PROPERTY RIGHTS ****************************#
#*                                                                                    *#
#*                           Copyright (c) 2025 Terminus LLC                          *#
#*                                                                                    *#
#*                                All Rights Reserved.                                *#
#*                                                                                    *#
#*          Use of this source code is governed by LICENSE in the repo root.          *#
#*                                                                                    *#
#**************************** INTELLECTUAL PROPERTY RIGHTS ****************************#
#
#    File:    conanfile.py
#    Author:  Marvin Smith
#    Date:    7/8/2023

from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps
from conan.tools.files import copy

class ConanProject(ConanFile):

    name = "terminus_log"
    version = "1.0.2"

    license = "Terminus Proprietary"
    author  = "Marvin Smith <marvin_smith1@me.com>"
    url     = "https://github.com/Terminus-Geospatial/terminus_log"
    description = "Standardized, extensible, and customizable logging"
    topics = ("terminus","log")

    implements = ["auto_header_only"]

    options = { "shared": [True, False],
                "with_tests": [True, False],
                "with_docs": [True, False],
                "with_coverage": [True, False]
    }

    default_options = { "shared": True,
                        "with_tests": True,
                        "with_docs": True,
                        "with_coverage": False,
                        "boost/*:shared": True
    }

    settings = "os", "compiler", "build_type", "arch"

    def build_requirements(self):
        # Build Dependencies
        self.build_requires("cmake/4.1.2")
        self.test_requires("gtest/1.17.0")

        # Tool Dependencies
        self.tool_requires("terminus_cmake/1.0.10")

    def requirements(self):
        self.requires("boost/1.89.0")

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.configure()
        return cmake

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["CONAN_PKG_NAME"]        = self.name
        tc.variables["CONAN_PKG_VERSION"]     = self.version
        tc.variables["CONAN_PKG_DESCRIPTION"] = self.description
        tc.variables["CONAN_PKG_URL"]         = self.url

        tc.variables["TERMINUS_LOG_ENABLE_TESTS"]    = self.options.with_tests
        tc.variables["TERMINUS_LOG_ENABLE_DOCS"]     = self.options.with_docs
        tc.variables["TERMINUS_LOG_ENABLE_COVERAGE"] = self.options.with_coverage

        tc.variables["TERMINUS_LOG_SOURCE_LOCATION_METHOD"] = "2"

        tc.generate()

        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        # For header-only packages, libdirs and bindirs are not used
         # so it's necessary to set those as empty.
         self.cpp_info.bindirs = []
         self.cpp_info.libdirs = []

    def export_sources(self):

        for p in [ "CMakeLists.txt", "library/include/*", "templates/*", "test/*", "README.md" ]:
            copy( self,
                  p,
                  self.recipe_folder,
                  self.export_sources_folder )
