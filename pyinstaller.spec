# -*- mode: python -*-
import os

project_path = os.path.dirname(os.path.abspath(SPEC))
added_data = [('assets', 'assets')]
icon_path = 'assets\\images\\helmet-icon.ico'
file_name = 'stick-bop'
app_name = 'stick-bop.app'

block_cipher = None

a = Analysis(['stick-bop.py'],
             pathex=project_path,
             binaries=[],
             datas=added_data,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name=file_name,
          icon=icon_path,
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False)
app = BUNDLE(exe,
             name=app_name,
             icon=None,
             bundle_identifier=None)
