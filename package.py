#!/usr/bin/env python3

import PyInstaller.__main__

PyInstaller.__main__.run([
    'src/email_draft_generator/gui/__main__.py',
    '--onedir',
    '--windowed',
    '-n',
    'E-mail Draft Generator',
    '--noconfirm',
    '--icon',
    'assets/icon.png',
])
