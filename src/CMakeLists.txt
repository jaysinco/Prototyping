function(single_file_exe_with_prefix)
    set(RAW_EXE_NAME ${ARGV0}-${ARGV1})
    string(REPLACE "/" "-" EXE_NAME ${RAW_EXE_NAME})
    add_executable(${EXE_NAME} ${ARGV1}.cpp)
    math(EXPR LIBS_ARGC "${ARGC}-2")
    list(SUBLIST ARGN 2 ${LIBS_ARGC} DEP_LIBS)
    target_link_libraries(${EXE_NAME} ${DEP_LIBS})
endfunction()

macro(single_file_executable)
    single_file_exe_with_prefix(${MAIN} ${ARGN})
endmacro()

add_subdirectory(utils)
add_subdirectory(parser)
add_subdirectory(test)
