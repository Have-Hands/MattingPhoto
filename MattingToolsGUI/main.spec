# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main.py','custom_widgets.py','main_gui.py','openvino_test.py','ui_thread.py'],
             pathex=['D:\\gitLearning\\MattingToolsGUI'],
             binaries=[],
             datas=[('D:\\Tools\\vinoviono\\openvino_2021\\inference_engine\\bin\\intel64\\Release', '.')],
             hiddenimports=['PyQt5','openvino.inference_engine.constants'],
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
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
		  icon='D:\\gitLearning\\MattingToolsGUI\\test.ico')

