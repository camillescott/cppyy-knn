cmake_minimum_required(VERSION 3.12)

project(cppyy_knn
        LANGUAGES CXX 
        VERSION 0.1 
        HOMEPAGE_URL "https://github.com/camillescott/cppyy-knn"
        DESCRIPTION "example cppyy bindings for a simple knn implementation")

if(DEFINED ENV{CONDA_PREFIX})
    message(STATUS "Building in a conda environment.")
    set(CONDA_ACTIVE TRUE)
    set(CMAKE_INSTALL_PREFIX "$ENV{CONDA_PREFIX}")
    set(CMAKE_PREFIX_PATH "$ENV{CONDA_PREFIX}")
    set(CMAKE_INCLUDE_PATH "$ENV{CONDA_PREFIX}/include")
    #include_directories($ENV{CONDA_PREFIX}/include)
    set(CMAKE_LIBRARY_PATH "$ENV{CONDA_PREFIX}/lib")
endif()

set(CMAKE_INCLUDE_DIRECTORIES_BEFORE ON)

# headers are listed in a cmake file.
include(${CMAKE_SOURCE_DIR}/manifest.cmake)
include(GNUInstallDirs)

# we want the conda includes if we're in a conda environment.
#

#
# Add our project's cmake dir the the module path. This gives us the
# Cppyy commands and targets.
#
list(INSERT CMAKE_MODULE_PATH 0 ${CMAKE_SOURCE_DIR}/cmake)
find_package(Cppyy)

#
# Make the default build us c++14 and "RELEASE" (-O3)
#
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
if(NOT CMAKE_BUILD_TYPE) 
    set(CMAKE_BUILD_TYPE Release)
endif(NOT CMAKE_BUILD_TYPE)

#
# Set up the knn shared lib
#
add_library(simpleknn
            SHARED
            ${LIB_SOURCES}
)
set_target_properties(simpleknn PROPERTIES LINKER_LANGUAGE CXX)
set_target_properties(simpleknn PROPERTIES
                      VERSION ${PROJECT_VERSION}
                      SOVERSION 1
)
set_target_properties(simpleknn PROPERTIES PUBLIC_HEADER ${LIB_HEADERS})
target_include_directories(simpleknn
                           PUBLIC
                           ${CMAKE_SOURCE_DIR}/src
)


#
# Set up the Cppyy bindings generation. This is a customized version defined
# in boink's cmake/ dir; it uses genreflex rather than calling rootcling directly.
# I did this because I couldn't get rootcling to properly include/exclude classes
# via the LinkDef header, and I wanted to be able to use the better syntax in
# the genreflex selection XML anyhow. Also, I think this is now the recommended /
# more modern way anyhow? Code was modified from the versions cppyy distributes.
#
cppyy_add_bindings(
   "cppyy_simpleknn" "${PROJECT_VERSION}" "Camille Scott & @jclay" "cswel@ucdavis.edu"
   LICENSE "MIT"
   LANGUAGE_STANDARD "14"
   SELECTION_XML  ${CMAKE_SOURCE_DIR}/selection.xml
   INTERFACE_FILE ${CMAKE_SOURCE_DIR}/src/nearest_neighbors.h
   HEADERS        ${LIB_HEADERS} 
   INCLUDE_DIRS   ${CMAKE_SOURCE_DIR}/src
   LINK_LIBRARIES simpleknn
)

add_executable(knn ${CMAKE_SOURCE_DIR}/src/main.cpp)
target_link_libraries(knn PUBLIC simpleknn)


install(TARGETS       simpleknn
        LIBRARY       DESTINATION ${CMAKE_INSTALL_LIBDIR}
        PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
)

install(CODE "execute_process(COMMAND pip install ${PY_WHEEL_FILE})")
