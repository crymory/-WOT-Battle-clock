
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
