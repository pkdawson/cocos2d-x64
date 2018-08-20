rd /s /q hello.build
mkdir hello.build
pushd hello.build
cmake -G "Visual Studio 15 2017 Win64" -DCOCOS_PATH=..\build\cocos2d-x -DCCBUILD_PATH=..\build\ccbuild -DVCPKG_PATH=..\build\vcpkg\installed\x64-windows-static ..\hello
cmake --build . --config Release
start Release\hello.exe
popd
