# -*- mode: python ; coding: utf-8 -*-

import os
import sys

block_cipher = None

# Base path of sync-service
base_dir = os.path.abspath(SPECPATH)

datas = [
    (os.path.join(base_dir, 'app', 'data', 'catalog_pack_rules.json'), os.path.join('app', 'data')),
]

hiddenimports = [
    # Uvicorn server runtime
    'uvicorn',
    'uvicorn.config',
    'uvicorn.main',
    'uvicorn.logging',
    'uvicorn.loops',
    'uvicorn.loops.auto',
    'uvicorn.loops.asyncio',
    'uvicorn.protocols',
    'uvicorn.protocols.http',
    'uvicorn.protocols.http.auto',
    'uvicorn.protocols.http.h11_impl',
    'uvicorn.protocols.http.httptools_impl',
    'uvicorn.protocols.websockets',
    'uvicorn.protocols.websockets.auto',
    'uvicorn.protocols.websockets.websockets_impl',
    'uvicorn.lifespans',
    'uvicorn.lifespans.auto',
    'uvicorn.lifespans.on',
    'uvicorn.lifespans.off',
    # FastAPI & Starlette
    'fastapi',
    'fastapi.routing',
    'fastapi.middleware.cors',
    'starlette',
    'starlette.routing',
    'starlette.responses',
    'pydantic',
    'pydantic_settings',
    'yaml',
    'websockets',
    'httpx',
    'sqlite3',
    # Tkinter UI
    'tkinter',
    'tkinter.ttk',
    'tkinter.filedialog',
    'tkinter.messagebox',
    'tkinter.scrolledtext',
    # Application modules
    'app',
    'app.api',
    'app.api.health',
    'app.api.sync',
    'app.api.orders',
    'app.api.import_api',
    'app.config',
    'app.logging_config',
    'app.db',
    'app.db.database',
    'app.dbf',
    'app.dbf.reader',
    'app.services',
    'app.services.master_service',
    'app.services.order_service',
    'app.services.exporter',
    'app.services.pack_resolver',
    'app.desktop',
    'app.desktop.settings',
    'app.desktop.validator',
    'app.desktop.server_runner',
    'app.desktop.ui',
    'app.desktop.launcher',
]

a = Analysis(
    ['app/desktop/launcher.py'],
    pathex=[base_dir],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
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
    name='PYROJA-Control-Panel',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
