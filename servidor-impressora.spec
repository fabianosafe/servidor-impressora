# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['servidor-impressora.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'win32print',
        'win32con',
        'pyperclip',
        'flask',
        'flask_cors',
        'tkinter',
        'tkinter.ttk',
        'tkinter.scrolledtext',
        'tkinter.messagebox',
        'threading',
        'json',
        'datetime',
        'webbrowser',
        'winreg',
        'pystray',
        'pystray._win32',
        'PIL',
        'PIL.Image',
        'PIL.ImageDraw',
    ],
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

# onedir (não onefile): o .exe fica numa pasta ao lado dos DLLs/dados, sem se
# autoextrair pra uma pasta temporária a cada execução — esse padrão de
# "autoextração" é um gatilho clássico de heurística de antivírus (parece
# comportamento de dropper de malware). UPX também desligado pelo mesmo motivo
# (binário compactado/ofuscado é outro gatilho comum).
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='servidor-impressora',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,  # Sem console (interface gráfica)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Adicione um ícone aqui se desejar
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='servidor-impressora',
)