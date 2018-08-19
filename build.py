from __future__ import print_function
import os
import sys
import subprocess
import contextlib
import shutil
import fileinput

# COCOS_COMMIT = 'eae47d008d66a9998bd2a25e6577415b52712557' # 3.17
COCOS_COMMIT = '925b727bb1f181b0e3b23a495b06b8dd0147dbda' # 2018-08-17

VCPKG_TRIPLET = 'x64-windows-static'
CMAKE_MSVS = 'Visual Studio 15 2017 Win64'

patch_dir = os.getcwd()
vcpkg_dir = os.path.join(os.getcwd(), 'build', 'vcpkg', 'installed', VCPKG_TRIPLET)
vcpkg_lib = os.path.join(vcpkg_dir, 'lib')

def call(cmd):
    if subprocess.call(cmd, shell=True) != 0:
        raise Exception(cmd)

@contextlib.contextmanager
def setdir(new_dir):
    previous_dir = os.getcwd()
    os.chdir(new_dir)
    yield
    os.chdir(previous_dir)

def sedi(fn, replacements):
    fi = fileinput.FileInput(fn, inplace=True, backup='.bak')
    for line in fi:
        for r in replacements.items():
            line = line.replace(r[0], r[1])
        print(line, end='')
    fi.close()

def fix_vcxproj(fn):
    sedi(fn, {
        'MultiThreadedDebugDLL' : 'MultiThreadedDebug',
        'MultiThreadedDLL' : 'MultiThreaded',
    })

def do_vcpkg():
    call('git clone https://github.com/Microsoft/vcpkg')
    with setdir('vcpkg'):
        call('bootstrap-vcpkg.bat')
        pkgs = 'bullet3 chipmunk freetype glew glfw3 libjpeg-turbo libvorbis mpg123 openal-soft tinyxml2 tiff libwebp sqlite3 flatbuffers xxhash'
        call('vcpkg --triplet {} install {}'.format(VCPKG_TRIPLET, pkgs))

    # this seemed easier than adding lzma.lib as an extra dependency?
    with setdir(vcpkg_lib):
        call('lib /OUT:tmp.lib tiff.lib lzma.lib')
        os.rename('tiff.lib', 'tiff.lib.bak')
        os.rename('tmp.lib', 'tiff.lib')

def build_openssl():
    call('git clone https://github.com/openssl/openssl')
    with setdir('openssl'):
        call('git checkout 97c0959f27b294fe1eb10b547145ebef2524b896')
        call('perl Configure VC-WIN64A no-asm no-shared --prefix={0} --openssldir={0}/SSL'.format(vcpkg_dir))
        call('nmake install')

def build_curl():
    call('git clone https://github.com/curl/curl')
    with setdir('curl'):
        call('git checkout eb8138405a3f747f2c236464932f72e918946f68')
    
    os.mkdir('curl.build')
    with setdir('curl.build'):
        call('cmake -G "Visual Studio 15 2017 Win64" -DBUILD_TESTING=OFF -DENABLE_MANUAL=OFF -DCMAKE_USE_OPENSSL=ON -DCURL_STATICLIB=ON -DCURL_STATIC_CRT=ON -DHTTP_ONLY=ON -DCMAKE_PREFIX_PATH="{0}" -DCMAKE_INSTALL_PREFIX="{0}" ../curl'.format(vcpkg_dir))
        call('cmake --build . --config Release --target install')

def build_libwebsockets():
    call('git clone https://github.com/warmcat/libwebsockets')
    with setdir('libwebsockets'):
        call('git checkout eaa935a80adb38b5cc4d09ce06ec987b87dcddfa')

    os.mkdir('libwebsockets.build')
    with setdir('libwebsockets.build'):
        call('cmake -G "{0}" -DCMAKE_PREFIX_PATH={1} -DCMAKE_INSTALL_PREFIX={1} -DLWS_WITHOUT_TESTAPPS=ON -DLWS_WITH_SHARED=OFF ../libwebsockets'.format(CMAKE_MSVS, vcpkg_dir))
        
        # use /MT instead of /MD
        fix_vcxproj('websockets.vcxproj')

        call('cmake --build . --config Release --target install')
        shutil.copy(os.path.join(vcpkg_lib, 'websockets_static.lib'), os.path.join(vcpkg_lib, 'websockets.lib'))

def build_chipmunk():
    call('git clone https://github.com/slembcke/Chipmunk2D')
    with setdir('Chipmunk2D'):
        call('git checkout 6b5b827a1c739437ba191dde5cf2446648417b82')

        # Release SCRT is mistakenly configured as DLL
        call('git apply {}/cp.patch'.format(patch_dir))

        call('msbuild msvc/vc14/chipmunk/chipmunk.vcxproj /p:Configuration="Release SCRT"')
        shutil.copy(os.path.join('msvc', 'vc14', 'chipmunk', 'x64', 'Release SCRT', 'chipmunk.lib'), vcpkg_lib)

def cocos_fetch():
    call('git clone https://github.com/cocos2d/cocos2d-x')
    with setdir('cocos2d-x'):
        call('git checkout {}'.format(COCOS_COMMIT))
        call('{} download-deps.py --remove-download=no'.format(sys.executable))

def cocos_prep():
    with setdir('cocos2d-x/external'):
        dirs = [
            'Box2D',
            'bullet',
            'chipmunk',
            'curl',
            'freetype2',
            'glfw3',
            'jpeg',
            'lua/luajit/prebuilt',
            'openssl',
            'png',
            'spidermonkey/prebuilt',
            'sqlite3',
            'tiff',
            'tinyxml2',
            'webp',
            'websockets',
            'win32-specific',
        ]
        for d in dirs:
            try:
                shutil.rmtree(d)
            except:
                pass

    with setdir('cocos2d-x'):
        call('git apply {}/cc.patch'.format(patch_dir))

        # use 64-bit Spidermonkey
        sedi('external/spidermonkey/include/win32/js-config.h', {
             '#define JS_NUNBOX32 1' : '#define JS_PUNBOX64 1',
        })

def cocos_cmake():
    try:
        shutil.rmtree('ccbuild')
    except:
        pass
    os.mkdir('ccbuild')
    with setdir('ccbuild'):
        call('cmake -G "{}" -DUSE_EXTERNAL_PREBUILT=OFF -DGEN_COCOS_PREBUILT=ON -DDEBUG_MODE=OFF -DCMAKE_PREFIX_PATH={} ../cocos2d-x'.format(CMAKE_MSVS, vcpkg_dir))
        call('cmake --build . --config Release --target cpp-tests')


def main():
    os.mkdir('build')
    os.chdir('build')
    do_vcpkg()
    build_openssl()
    build_curl()
    build_libwebsockets()
    build_chipmunk()
    cocos_fetch()
    cocos_prep()
    cocos_cmake()
    call('ccbuild\\bin\\cpp-tests\\Release\\cpp-tests.exe')

if __name__ == '__main__':
    if sys.version_info[0] > 2:
        print('Please run with Python 2.7, as required by cocos2d-x')
    else:
        main()
