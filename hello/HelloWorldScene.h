#pragma once

#pragma warning(push, 0)
#include "cocos2d.h"
#pragma warning(pop)

class HelloWorld : public cocos2d::Scene
{
public:
    virtual bool init() override;

    static cocos2d::Scene* scene();

    CREATE_FUNC(HelloWorld);
};
