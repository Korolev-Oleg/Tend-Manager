# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['.'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

a.datas += [
          ('add.ico','.\\interface\\icons\\add.ico','DATA'),
          ('arrow-right.ico','.\\interface\\icons\\arrow-right.ico','DATA'),
          ('clear.ico','.\\interface\\icons\\clear.ico','DATA'),
          ('display-none.ico','.\\interface\\icons\\display-none.ico','DATA'),
          ('docs.ico','.\\interface\\icons\\docs.ico','DATA'),
          ('info.ico','.\\interface\\icons\\info.ico','DATA'),
          ('logo.ico','.\\interface\\icons\\logo.ico','DATA'),
          ('new-item.ico','.\\interface\\icons\\new-item.ico','DATA'),
          ('remove.ico','.\\interface\\icons\\remove.ico','DATA'),
          ('settings.ico','.\\interface\\icons\\settings.ico','DATA'),
          ]          


pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False, icon='.\\interface\\icons\\logo.ico' )
