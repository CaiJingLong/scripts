#!/bin/sh

if [ -z "$1" ]; then
    echo "Usage: $0 <apk_path>"
    exit 1
fi

# 在华为上使用adb命令跳过“纯净模式”并安装apk

adb shell pm disable-user com.android.packageinstaller
adb install -r $1
adb shell pm enable com.android.packageinstaller
