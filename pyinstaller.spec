# -*- mode: python ; coding: utf-8 -*-

import importlib.metadata

added_files = [
    ('assets/icon.png', 'email_draft_generator/gui/assets'),
    ('assets/icon_macos.png', 'email_draft_generator/gui/assets'),
]

a = Analysis(
    ['src/email_draft_generator/gui/__main__.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='E-mail Draft Generator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['assets/icon.png'],
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='E-mail Draft Generator',
)

app = BUNDLE(
    coll,
    name='E-mail Draft Generator.app',
    icon='assets/icon_macos.png',
    bundle_identifier=None,
    version=importlib.metadata.version('email-draft-generator'),
)
