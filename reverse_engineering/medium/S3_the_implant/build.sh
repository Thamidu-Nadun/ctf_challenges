#!/bin/sh

#  S3 — guardian_update build
# ---------------------------------------------------------------------
#  ELF build  -> dist/guardian_update_linux   
#  PE  build  -> dist/guardian_update.exe      

set -e
mkdir -p dist
SRC=src/guardian_update.c

# Linux ELF — test build 
gcc -O2 -s -o dist/guardian_update_linux "$SRC"

# Windows PE — the challenge artifact (stripped, 64-bit)
x86_64-w64-mingw32-gcc -O2 -s -o dist/guardian_update.exe "$SRC"

echo "[+] built:"
ls -la dist/guardian_update_linux dist/guardian_update.exe
file dist/guardian_update.exe
