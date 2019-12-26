# -*- mode: python ; coding: utf-8 -*-
from kivy_deps import sdl2, glew, angle

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
        ("logo.png", "."),
        ("pyproject.toml", "."),
        
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
    *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins + angle.dep_bins)],
    name="MyDevoirs",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    icon="logo.ico"
)
