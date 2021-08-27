#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include "utils.h"
#include <fstream>
#include <sstream>

namespace utils
{
std::string ws2s(const std::wstring &ws, bool u8_instead_of_ansi)
{
    UINT page = u8_instead_of_ansi ? CP_UTF8 : CP_ACP;
    int len = WideCharToMultiByte(page, 0, ws.c_str(), -1, nullptr, 0, nullptr, nullptr);
    if (len <= 0) return "";
    auto buf = new char[len]{0};
    if (buf == nullptr) return "";
    WideCharToMultiByte(page, 0, ws.c_str(), -1, buf, len, nullptr, nullptr);
    std::string s = buf;
    delete[] buf;
    return s;
}

std::wstring s2ws(const std::string &s, bool u8_instead_of_ansi)
{
    UINT page = u8_instead_of_ansi ? CP_UTF8 : CP_ACP;
    int len = MultiByteToWideChar(page, 0, s.c_str(), -1, nullptr, 0);
    if (len <= 0) return L"";
    auto buf = new wchar_t[len]{0};
    if (buf == nullptr) return L"";
    MultiByteToWideChar(page, 0, s.c_str(), -1, buf, len);
    std::wstring ws = buf;
    delete[] buf;
    return ws;
}

std::pair<bool, std::string> readFile(const std::wstring &path)
{
    std::ifstream in_file(path);
    if (!in_file) {
        return {false, ""};
    }
    std::stringstream ss;
    ss << in_file.rdbuf();
    return {true, ss.str()};
}

std::wstring getExePath()
{
    wchar_t buf[MAX_PATH + 1] = {0};
    GetModuleFileNameW(NULL, buf, MAX_PATH);
    (wcsrchr(buf, L'\\'))[0] = 0;
    return buf;
}

}  // namespace utils
