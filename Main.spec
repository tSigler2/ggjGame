# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['GameLib\\Main.py'],
    pathex=[],
    binaries=[],
    datas=[('GameLib\\CodeRunnerFile.py', '.\\'), ('GameLib\\Coral.py', '.\\'), ('GameLib\\CoralManager.py', '.\\'), ('GameLib\\Enemy.py', '.\\'), ('GameLib\\EnemyManager.py', '.\\'), ('GameLib\\Game.py', '.\\'), ('GameLib\\House.py', '.\\'), ('GameLib\\Level1.py', '.\\'), ('GameLib\\Main.py', '.\\'), ('GameLib\\MainMenu.py', '.\\'), ('GameLib\\Map.py', '.\\'), ('GameLib\\MapSlot.py', '.\\'), ('GameLib\\Player.py', '.\\'), ('GameLib\\Settings.py', '.\\'), ('GameLib\\Test.py', '.\\'), ('GameLib\\__init__.py', '.\\'), ('GameLib\\Assets\\background.png', '.\\Assets'), ('GameLib\\Assets\\house.png', '.\\Assets'), ('GameLib\\Assets\\IMG_2186.png', '.\\Assets'), ('GameLib\\Assets\\SandGrid.png', '.\\Assets'), ('GameLib\\Assets\\Sand_tile.png', '.\\Assets'), ('GameLib\\Assets\\coral\\std\\coral1.png', '.\\Assets\\coral\\std'), ('GameLib\\Assets\\coral\\std\\coral2.png', '.\\Assets\\coral\\std'), ('GameLib\\Assets\\coral\\std\\coral3.png', '.\\Assets\\coral\\std'), ('GameLib\\Assets\\coral\\std\\coral4.png', '.\\Assets\\coral\\std'), ('GameLib\\Assets\\FishDeathSounds\\FishDeath_07.wav', '.\\Assets\\FishDeathSounds'), ('GameLib\\Assets\\FishDeathSounds\\FishDeath_11.wav', '.\\Assets\\FishDeathSounds'), ('GameLib\\Assets\\FishDeathSounds\\FishDeath_15.wav', '.\\Assets\\FishDeathSounds'), ('GameLib\\Assets\\FishDeathSounds\\FishDeath_22.wav', '.\\Assets\\FishDeathSounds'), ('GameLib\\Assets\\music\\Squirrely Pop MainTheme.mp3', '.\\Assets\\music'), ('GameLib\\Assets\\player\\attack\\JimmyBite1.png', '.\\Assets\\player\\attack'), ('GameLib\\Assets\\player\\attack\\JimmyBite2.png', '.\\Assets\\player\\attack'), ('GameLib\\Assets\\player\\attack\\JimmyBite3.png', '.\\Assets\\player\\attack'), ('GameLib\\Assets\\player\\attack\\JimmyBite4.png', '.\\Assets\\player\\attack'), ('GameLib\\Assets\\player\\attack\\JimmyBite5.png', '.\\Assets\\player\\attack'), ('GameLib\\Assets\\player\\attack\\JimmyBite6.png', '.\\Assets\\player\\attack'), ('GameLib\\Assets\\player\\walk\\JimmyWalkcycle1.png', '.\\Assets\\player\\walk'), ('GameLib\\Assets\\player\\walk\\JimmyWalkcycle2.png', '.\\Assets\\player\\walk'), ('GameLib\\Assets\\sounds\\TownTheme.mp3', '.\\Assets\\sounds'), ('GameLib\\Assets\\squirrel\\attack\\SquirelEnemyAttack01.png', '.\\Assets\\squirrel\\attack'), ('GameLib\\Assets\\squirrel\\attack\\SquirelEnemyAttack02.png', '.\\Assets\\squirrel\\attack'), ('GameLib\\Assets\\squirrel\\attack\\SquirelEnemyAttack03.png', '.\\Assets\\squirrel\\attack'), ('GameLib\\Assets\\squirrel\\attack\\SquirelEnemyAttack04.png', '.\\Assets\\squirrel\\attack'), ('GameLib\\Assets\\squirrel\\attack\\SquirelEnemyAttack05.png', '.\\Assets\\squirrel\\attack'), ('GameLib\\Assets\\squirrel\\attack\\SquirelEnemyAttack06.png', '.\\Assets\\squirrel\\attack'), ('GameLib\\Assets\\squirrel\\attack\\SquirelEnemyAttack07.png', '.\\Assets\\squirrel\\attack'), ('GameLib\\Assets\\squirrel\\attack\\SquirelEnemyAttack08.png', '.\\Assets\\squirrel\\attack'), ('GameLib\\Assets\\squirrel\\attack\\SquirelEnemyAttack09.png', '.\\Assets\\squirrel\\attack'), ('GameLib\\Assets\\squirrel\\attack\\SquirelEnemyAttack10.png', '.\\Assets\\squirrel\\attack'), ('GameLib\\Assets\\squirrel\\attack\\SquirelEnemyAttack11.png', '.\\Assets\\squirrel\\attack'), ('GameLib\\Assets\\squirrel\\attack\\SquirelEnemyAttack12.png', '.\\Assets\\squirrel\\attack'), ('GameLib\\Assets\\squirrel\\attack\\SquirelEnemyAttack13.png', '.\\Assets\\squirrel\\attack'), ('GameLib\\Assets\\squirrel\\walk\\SquirelEnemy1.png', '.\\Assets\\squirrel\\walk'), ('GameLib\\Assets\\squirrel\\walk\\SquirelEnemy2.png', '.\\Assets\\squirrel\\walk'), ('GameLib\\Assets\\squirrel\\walk\\SquirelEnemy3.png', '.\\Assets\\squirrel\\walk'), ('GameLib\\Assets\\squirrel\\walk\\SquirelEnemy4.png', '.\\Assets\\squirrel\\walk'), ('GameLib\\Menu\\Button.py', '.\\Menu'), ('GameLib\\Menu\\__init__.py', '.\\Menu'), ('GameLib\\Sprite\\AnimatedSprite.py', '.\\Sprite'), ('GameLib\\Sprite\\MultiAnimatedSprite.py', '.\\Sprite'), ('GameLib\\Sprite\\Sprite.py', '.\\Sprite'), ('GameLib\\Sprite\\__init__.py', '.\\Sprite'), ('GameLib\\StdObj\\CollidableObj.py', '.\\StdObj'), ('GameLib\\StdObj\\MoveableObj.py', '.\\StdObj'), ('GameLib\\StdObj\\StdEntity.py', '.\\StdObj'), ('GameLib\\Util\\Sound.py', '.\\Util'), ('GameLib\\Util\\__init__.py', '.\\Util')],
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
    a.binaries,
    a.datas,
    [],
    name='Main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
