from conans import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, CMakeDeps
import os
import sys


class PrototypingConan(ConanFile):
    name = "prototyping"
    version = "0.1.0"
    url = "https://github.com/JaySinco/conan"
    homepage = "https://github.com/JaySinco/Prototyping"
    description = "C++ prototype repo"
    license = "MIT"

    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "gflags:nothreads": False,
    }

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            del self.options.fPIC

    def requirements(self):
        self.requires("spdlog/1.10.0@jaysinco/stable")
        self.requires("boost/1.79.0@jaysinco/stable")
        self.requires("glfw/3.3.7@jaysinco/stable")
        self.requires("implot/0.13@jaysinco/stable")
        self.requires("expected-lite/0.5.0@jaysinco/stable")
        self.requires("catch2/2.13.9@jaysinco/stable")
        self.requires("mujoco/2.2.2@jaysinco/stable")
        self.requires("torch/1.8.2@jaysinco/stable")
        self.requires("qt/5.15.3@jaysinco/stable")
        self.requires("folly/v2022.01.31.00@jaysinco/stable")

    def layout(self):
        build_folder = "out"
        build_type = str(self.settings.build_type)
        self.folders.source = ""
        self.folders.build = os.path.join(build_folder, build_type)
        self.folders.generators = os.path.join(
            self.folders.build, "generators")

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["CMAKE_RUNTIME_OUTPUT_DIRECTORY_DEBUG"] = self._normalize_path(
            os.path.join(self.source_folder, "bin"))
        tc.variables["CMAKE_RUNTIME_OUTPUT_DIRECTORY_RELEASE"] = self._normalize_path(
            os.path.join(self.source_folder, "bin", "Release"))
        self._setup_pkg_root(tc)
        tc.generate()
        cmake_deps = CMakeDeps(self)
        cmake_deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def _setup_pkg_root(self, tc):
        for pkg in self.deps_cpp_info._dependencies:
            root = "{}_ROOT".format(pkg)
            tc.variables[root] = self._normalize_path(
                self.deps_cpp_info[pkg].cpp_info.rootpath)

    def _normalize_path(self, path):
        if self.settings.os == "Windows":
            return path.replace("\\", "/")
        else:
            return path
