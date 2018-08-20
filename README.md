# cocos2d-x64

A quick and dirty script to build cocos2d-x for 64-bit Windows, with static libraries and linked to the static runtime.
Some stuff is probably broken, js-tests and lua-tests don't build, but cpp-tests seems fine and that's all I need.

Only builds the release libraries, not debug.

Uses a recent Git version of cocos2d-x (2018-08-17) instead of 3.17, mostly to fix a bug with cocos_copy_res.

I build most libraries with vcpkg, but vcpkg has an old version of OpenSSL and a broken Chipmunk (in static configuration),
so I need to build some stuff manually.

## Prerequisites

* Visual Studio 2017
    * Desktop development with C++
    * Windows 8.1 SDK
* Strawberry Perl (for building OpenSSL)
* Python 2.7

## Building

I'd strongly recommend looking at the script (and the patch), seeing what it does, and adapting it to your needs
instead of simply running it. It's not robust or user-friendly. But this should work:

1. Open an x64 Native Tools Command Prompt for VS 2017
2. Run `C:\Python27\python.exe build.py`
