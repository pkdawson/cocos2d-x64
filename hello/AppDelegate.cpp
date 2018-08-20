#include "AppDelegate.h"
#include "HelloWorldScene.h"

USING_NS_CC;
using namespace std;

AppDelegate::AppDelegate()
{
}

AppDelegate::~AppDelegate()
{
}

void AppDelegate::initGLContextAttrs()
{
    GLContextAttrs glContextAttrs = { 8, 8, 8, 8, 24, 8, 0 };

    GLView::setGLContextAttrs(glContextAttrs);
}

bool AppDelegate::applicationDidFinishLaunching()
{
    auto director = Director::getInstance();
    auto glview = director->getOpenGLView();
    if (!glview) {
        glview = GLViewImpl::create("Hello Win64");
        director->setOpenGLView(glview);
    }

    director->setOpenGLView(glview);

    glview->setDesignResolutionSize(1024, 768, ResolutionPolicy::NO_BORDER);

    director->setDisplayStats(true);
    director->setAnimationInterval(1.0f / 60);

    auto scene = HelloWorld::scene();
    director->runWithScene(scene);

    return true;
}

void AppDelegate::applicationDidEnterBackground()
{
    Director::getInstance()->stopAnimation();
}

void AppDelegate::applicationWillEnterForeground()
{
    Director::getInstance()->startAnimation();
}
