from conans import ConanFile
import os
from conans.tools import download
from conans.tools import unzip
from conans import CMake


class PugiConan(ConanFile):
    name = "pugixml"
    ZIP_FOLDER_NAME = "pugixml-1.7"
    version = "1.7"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    exports = "CMakeLists.txt"
    requires = "gtest/1.8.0@lms/stable"
    generators = "cmake"

    def source(self):
        zip_name = "%s.zip" % self.ZIP_FOLDER_NAME
        url = "https://github.com/zeux/pugixml/releases/download/v1.7/pugixml-1.7.zip"
        download(url, zip_name)
        unzip(zip_name)
        os.unlink(zip_name)


    def build(self):
        cmake = CMake(self.settings)
        if self.settings.os == "Windows":
            self.run("IF not exist _build mkdir _build")
        else:
            self.run("mkdir _build")
        cd_build = "cd _build"
        force = "-Dgtest_force_shared_crt=ON"
        shared = "-DBUILD_SHARED_LIBS=1" if self.options.shared else ""
        self.run('%s && cmake .. %s %s %s' % (cd_build, cmake.command_line, shared, force))
        self.run("%s && cmake --build . %s" % (cd_build, cmake.build_config))

    def package(self):
        # Copying headers
        self.copy(pattern="*.hpp", dst="include", src="%s/src" %self.ZIP_FOLDER_NAME, keep_path=True)

        # Copying static and dynamic libs
        self.copy(pattern="*.a", dst="lib", src=".", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", src=".", keep_path=False)
        self.copy(pattern="*.dll", dst="bin", src=".", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", src=".", keep_path=False)
        self.copy(pattern="*.dylib*", dst="lib", src=".", keep_path=False)  

    def package_info(self):
        self.cpp_info.libs = ["pugixml"]
