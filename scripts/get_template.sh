#!/usr/bin/env bash
echo 'create empty git'
git init
mkdir temp
cd temp
git clone 'https://github.com/code-datum/telegram-bot-main-example.git' git
cd git
cp -rf . ../../
cd ../../
rm -rf temp/git
echo 'Git clone is finished'
