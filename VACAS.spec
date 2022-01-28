# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

a = Analysis(['vacas/VACAS.py'],
             pathex=['usr/local/bin/python3','/Users/qxz0n5g/Desktop/VACAS/vacas'],
             binaries=[],
             datas=[('vacas/resources','./resources'),('vacas/config.yaml','.')],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

#splash = Splash('vacas/resources/images/vacas_splash.png',
#                binaries=a.binaries,
#                datas=a.datas,
#                text_pos=(10, 50),
#                text_size=12,
#                text_color='black')

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts, 
          [],
          icon='vacas/resources/icons/cow.ico',
          exclude_binaries=True,
          name='VACAS',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='VACAS')

app = BUNDLE(   coll,
                name='VACAS.app',
                icon='vacas/resources/icons/cow.icns',
                bundle_identifier=None,
                version='0.3',
                info_plist={
                    'NSPrincipalClass': 'NSApplication',
                    'NSAppleScriptEnabled': False,
                    'CFBundleDocumentTypes': [
                        {
                            'CFBundleTypeName': 'My File Format',
                            'CFBundleTypeIconFile': 'MyFileIcon.icns',
                            'LSItemContentTypes': ['com.example.myformat'],
                            'LSHandlerRank': 'Owner'
                        }
                    ]
                },
            )