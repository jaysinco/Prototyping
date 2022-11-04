#include "utils/base.h"
#include <bshoshany/BS_thread_pool.hpp>

int main(int argc, char** argv)
{
    BS::thread_pool pool;
    std::future<int> my_future = pool.submit([] { return 42; });
    spdlog::info(my_future.get());
}
