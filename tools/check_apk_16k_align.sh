#!/bin/bash
# 检查 APK 中的 so 文件是否支持 16K 对齐
# 用法: ./check_apk_16k_align.sh <your.apk>
# 依赖：unzip, readelf
# 依赖安装：brew install binutils unzip

alias readelf="/opt/homebrew/opt/binutils/bin/readelf"

if [ $# -ne 1 ]; then
  echo "用法: $0 <your.apk>"
  exit 1
fi

APK_FILE="$1"
TMP_DIR="/tmp/apk_16k_align_check_$$"

# 检查依赖
command -v unzip >/dev/null 2>&1 || { echo >&2 "需要 unzip，请先安装。"; exit 1; }
command -v readelf >/dev/null 2>&1 || { echo >&2 "需要 readelf，请先安装（通常在 binutils 包中）。"; exit 1; }

mkdir "$TMP_DIR"
unzip -qq "$APK_FILE" -d "$TMP_DIR"

SO_FILES=$(find "$TMP_DIR" -type f -name '*.so')

if [ -z "$SO_FILES" ]; then
  echo "没有找到 so 文件。"
  rm -rf "$TMP_DIR"
  exit 1
fi

ALL_PASS=1

SUPPORT_FILES=""
UNSUPPORT_FILES=""

for SO in $SO_FILES; do
  echo "检查: $SO"
  ALIGN_LIST=$(readelf -l "$SO" | awk '/LOAD/ {getline; print $NF}')
  FOUND=0
  for ALIGN_HEX in $ALIGN_LIST; do
    ALIGN_DEC=$((ALIGN_HEX))
    echo "  LOAD段对齐: $ALIGN_HEX ($ALIGN_DEC)"
    if [ "$ALIGN_DEC" -eq 16384 ] || [ "$ALIGN_DEC" -eq 65536 ]; then
      FOUND=1
    fi
  done
  if [ $FOUND -eq 1 ]; then
    echo "  支持 16K 对齐"
    SUPPORT_FILES="$SUPPORT_FILES\n$SO"
  else
    echo "  不支持 16K 对齐!!! 当前是 $ALIGN_HEX" 
    UNSUPPORT_FILES="$UNSUPPORT_FILES\n$SO"
    ALL_PASS=0
  fi
done

rm -rf "$TMP_DIR"

if [ $ALL_PASS -eq 1 ]; then
  echo "\n所有 so 文件均支持 16K 对齐。"
else
  echo "\n存在不支持 16K 对齐的 so 文件，请检查上方输出。"
fi

if [ -n "$SUPPORT_FILES" ]; then
  echo "\n支持 16K 对齐的 so 文件："
  echo "$SUPPORT_FILES"
fi

if [ -n "$UNSUPPORT_FILES" ]; then
  echo "\n不支持 16K 对齐的 so 文件："
  echo "$UNSUPPORT_FILES"
fi
