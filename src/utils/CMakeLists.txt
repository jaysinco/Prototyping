get_filename_component(CURRENT_DIR_NAME ${CMAKE_CURRENT_SOURCE_DIR} NAME)
set(LIB ${CURRENT_DIR_NAME})

add_library(${LIB} base.cpp)
target_link_libraries(${LIB} PUBLIC
    spdlog::spdlog
    deps_expected-lite
)