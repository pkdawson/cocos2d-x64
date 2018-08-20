# This demonstrates a simplistic way to build a cocos2d-x game without
# using their project tools.

cmake_minimum_required(VERSION 3.8)
project(hello LANGUAGES CXX)

# set(CMAKE_CXX_STANDARD 17)
# set(CMAKE_CXX_STANDARD_REQUIRED ON)
# set(CMAKE_CXX_EXTENSIONS OFF)

set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} /MTd")
set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} /MT")
set(CMAKE_EXE_LINKER_FLAGS_DEBUG "${CMAKE_EXE_LINKER_FLAGS_DEBUG}")
set(CMAKE_EXE_LINKER_FLAGS_RELEASE "${CMAKE_EXE_LINKER_FLAGS_RELEASE}")

include_directories("${VCPKG_PATH}/include")
include_directories("${VCPKG_PATH}/include/GLFW")
link_directories("${VCPKG_PATH}/lib")

include_directories("${COCOS_PATH}/cocos")
link_directories("${CCBUILD_PATH}/lib/Release")

link_libraries(cocos2d freetype libcurl bz2 lzma glew32 glfw3 vorbisfile vorbis
    ogg libmpg123 OpenAL32 sqlite3 zlib tinyxml2 websockets flatbuffers xxhash
    libssl libcrypto jpeg webp tiff libpng16 chipmunk BulletDynamics BulletCollision
    LinearMath BulletSoftBody unzip recast opengl32 glu32 ws2_32 winmm Version Iphlpapi crypt32)

add_definitions(-DCC_STATIC)

add_executable(hello
    main.cpp
    AppDelegate.cpp AppDelegate.h
    HelloWorldScene.cpp HelloWorldScene.h
)

target_compile_options(hello PRIVATE /std:c++latest /permissive-)
