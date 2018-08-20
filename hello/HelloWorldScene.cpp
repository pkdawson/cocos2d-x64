#include "HelloWorldScene.h"

USING_NS_CC;

Scene* HelloWorld::scene()
{
    return HelloWorld::create();
}

bool HelloWorld::init()
{
    if (!Scene::init()) {
        return false;
    }

    auto visibleSize = Director::getInstance()->getVisibleSize();
    auto origin = Director::getInstance()->getVisibleOrigin();
    auto label = Label::createWithSystemFont("Hello Win64", "Arial", 96);

    // position the label on the center of the screen
    label->setPosition(origin.x + visibleSize.width / 2,
        origin.y + visibleSize.height - label->getContentSize().height);

    // add the label as a child to this layer
    this->addChild(label, 1);

    auto drawNode = DrawNode::create();
    drawNode->setPosition(Vec2(0, 0));
    addChild(drawNode);

    return true;
}
