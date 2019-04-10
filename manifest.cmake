set(_headers
    nearest_neighbors.h
)

set(_sources
    nearest_neighbors.cpp
)

foreach (path ${_headers})
    list(APPEND LIB_HEADERS ${CMAKE_SOURCE_DIR}/src/${path})
endforeach(path)

foreach (path ${_sources})
    list(APPEND LIB_SOURCES ${CMAKE_SOURCE_DIR}/src/${path})
endforeach(path)
