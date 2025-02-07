from pathlib import Path
import zipfile
import os

def create_wotmod():
    # Имя выходного файла
    wotmod_name = "battle_clock_1.0.0.wotmod"

    # Создаём временную структуру папок
    os.makedirs("temp/res/scripts/client/gui/mods", exist_ok=True)

    # Копируем код мода
    with open("temp/res/scripts/client/gui/mods/mod_battle_clock.py", "w", encoding="utf-8") as f:
        f.write("""
import BigWorld
import GUI
from gui.Scaleform.framework import ViewTypes
from gui.Scaleform.framework.entities.View import View
from gui.app_loader import g_appLoader
import time

class BattleClock(View):
    def __init__(self):
        super(BattleClock, self).__init__()
        self.clock = None
        self.call = None

    def _populate(self):
        super(BattleClock, self)._populate()
        self.clock = GUI.Text('')
        self.clock.visible = True
        self.clock.position = (0.85, 0.02, 0.3)
        self.clock.colour = (255, 255, 255, 255)
        GUI.addRoot(self.clock)
        self.update_time()

    def update_time(self):
        if self.clock is not None:
            current_time = time.strftime("%H:%M:%S")
            self.clock.text = current_time
            self.call = BigWorld.callback(1.0, self.update_time)

    def _dispose(self):
        if self.clock is not None:
            GUI.delRoot(self.clock)
            self.clock = None
        if self.call is not None:
            BigWorld.cancelCallback(self.call)
            self.call = None
        super(BattleClock, self)._dispose()

g_battleClock = None

def init():
    global g_battleClock
    g_battleClock = BattleClock()
    app = g_appLoader.getDefBattleApp()
    if app is not None:
        app.loadView(ViewTypes.WINDOW, g_battleClock)

def fini():
    global g_battleClock
    if g_battleClock is not None:
        g_battleClock._dispose()
        g_battleClock = None
""")

    # Создаём meta.xml
    with open("temp/meta.xml", "w", encoding="utf-8") as f:
        f.write("""<?xml version="1.0" encoding="utf-8"?>
<root>
    <id>battle_clock_mod</id>
    <version>1.0.0</version>
    <name>Battle Clock</name>
    <description>Shows current time in battle</description>
    <dependencies>
        <game>1.27.1</game>
    </dependencies>
</root>""")

    # Создаём .wotmod файл
    with zipfile.ZipFile(wotmod_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk("temp"):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, "temp")
                zipf.write(file_path, arcname)

    # Очищаем временные файлы
    import shutil
    shutil.rmtree("temp")

    print(f"Created {wotmod_name}")

if __name__ == "__main__":
    create_wotmod()
