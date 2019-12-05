# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(
    ["main.py"],
    pathex=["."],
    binaries=[],
    # datas=[("data/icons/*.png", "data/icons")],
    datas=[
        ("mydevoirs/*.kv", "mydevoirs"),
        ("data/icons/*.png", "data/icons"),
        ("data/fonts/*.ttf", "data/fonts"),
        ("data/fonts/*.otf", "data/fonts"),
        ("logo.png", "."),

    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="MyDevoirs",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    icon="logo.png"
)
