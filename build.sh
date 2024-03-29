#!/bin/bash

set -e

do_clean=0
do_preprocess=0
do_rm_cmake_cache=0
build_release=0

while [[ $# -gt 0 ]]; do
    case $1 in
        -h)
            echo
            echo "Usage: build.sh [options]"
            echo
            echo "Options:"
            echo "  -c   clean build"
            echo "  -e   remove cmake cache"
            echo "  -f   format & check code"
            echo "  -r   build release version (default: debug)"
            echo "  -h   print command line options"
            echo
            exit 0
            ;;
        -c) do_clean=1 && shift ;;
        -r) build_release=1 && shift ;;
        -f) do_preprocess=1 && shift ;;
        -e) do_rm_cmake_cache=1 && shift ;;
         *) echo "Unknown option: $1" && exit 1 ;;
    esac
done

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
git_root="$(git rev-parse --show-toplevel)"

build_type=Debug
if [ $build_release -eq 1 ]; then
    build_type=Release
fi

conan_profile=$git_root/config/conan.profile
build_folder=$git_root/out/$build_type

if [ $do_clean -eq 1 ]; then
    rm -rf $git_root/out $git_root/bin
fi

if [ $do_rm_cmake_cache -eq 1 ]; then
    rm -f $build_folder/CMakeCache.txt
fi

function preprocess_source() {
    if [ $do_preprocess -eq 1 ]; then
        find src -iname *.h -or -iname *.cpp | xargs clang-format -i \
        && find src -iname *.h -or -iname *.cpp | xargs \
            clang-tidy --quiet --warnings-as-errors="*" -p $build_folder
    fi
}

pushd $git_root \
&& preprocess_source \
&& conan install . \
    --install-folder=$build_folder \
    --profile=$conan_profile \
    --profile:build=$conan_profile \
    --settings=build_type=$build_type \
    --build=never \
&& conan build --install-folder=$build_folder . \
&& echo done!
