import tkinter
import ctypes
import platform

from os.path import abspath, join, dirname


class Controller:
    events = {
        'left_click':          '<Button-1>',
        'midle_click':         '<Button-2>',
        'right_click':         '<Button-3>',
        'scroll_up':           '<Button-4>',
        'scroll_down':         '<Button-5>',
        'db_right_click':      '<Double-Button-3',
        'db_midle_click':      '<Double-Button-2>',
        'db_left_click':       '<<Double-Button-1>',
        'move_with_left':      '<B1-Motion>',
        'move_with_midle':     '<B2-Motion>',
        'move_with_right':     '<B3-Motion>',
        'left_click_release':  '<ButtonRelease-1>',
        'midle_click_release': '<ButtonRelease-2>',
        'right_click_release': '<ButtonRelease-3>',
        'mousein':             '<Enter>',
        'mouseleave':          '<Leave>',
        'focus':               '<FocusIn>',
        'focus_leave':         '<FocusOut>',
        'onspecialkeys':       '<Return>',
        'keydown':             '<Key>',
        'shift_up':            '<Shift-Up>',
        'resize':              '<Configure>'
    }

    listeners = None

    def __init__(self, master):
        self.listeners = self.setMapOfEvenetHandler()
        self.master    = master

        self.addEventListeners()

    def addEventListeners(self):
        for event, action in self.listeners.items():
            self.addEventListener(event, action)

    def addEventListener(self, event, action):
        self.master.dom.bind(event, action)

    def setMapOfEvenetHandler(self):
        return {self.events[prop]: self.__getattribute__(prop)
            for prop in dir(self)
            if prop in self.events and callable(self.__getattribute__(prop))
        }



class Element(object):
    parentNode          = None
    dom                 = None
    items               = None
    packParams          = None
    gridParams          = None
    bg                  = None
    cursor              = None
    highlightbackground = None
    highlightcolor      = None
    highlightthickness  = None
    relief	            = None
    tk_type             = None
    column              = None
    columnspan          = None
    in_                 = None
    ipadx               = None
    ipady               = None
    padx                = None
    pady                = None
    listeners           = None
    row                 = None
    rowspan             = None
    sticky              = None
    controller          = None
    width               = 0
    height              = 0
    gridParams          = [
        "column", "columnspan",
        "in_", "ipadx", "ipady"
        "padx", "pady", "row"
        "rowspan", "sticky", "row"
    ]

    def __init__(self, compileParams, parentNode=None):
        for att, value in compileParams.items(): 
            if hasattr(self, att):
                self.__setattr__(att, value)

        self.parentNode = parentNode

    def getPackParams(self):
        return {k : self.__getattribute__(k)
            for  k in self.packParams
            if hasattr(self, k)
        }

    def getGridParams(self):
        return {k : self.__getattribute__(k)
            for  k in self.gridParams
            if hasattr(self, k) and not k is None
        }

    def render(self):
        self.dom.grid(**self.getGridParams())

    def getGeometry(self):
        return "%sx%s" % (self.width, self.height)

    def setController(self, controller):
        self.controller = controller(self)


class MainFrame(Element):
    width      = 100
    height     = 100
    title      = 'MainFrame'
    wizards    = []
    tk_type    = tkinter.Tk
    menu       = None
    ignored    = ['items']
    resizable  = None
    
    def __init__(self, compileParams, parentNode=None):
        if "menu" in compileParams:
            self.items = [compileParams["menu"]]

        super().__init__(compileParams)

    def render(self):
        self._setResizeble()
        self.dom.title(self.title)
        self.dom.geometry(self.getGeometry())
        self.dom.mainloop()
        
    def _setResizeble(self):
        if not self.resizable is None:
            if (isinstance(self.resizable, list)):
                self.dom.resizable(self.resizable[0], self.resizable[1])
            elif (not self.resizable):
                self.dom.resizable(False, False)


class Menu(Element):
    tk_type    = tkinter.Frame
    packParams = ["width", "height", "bg"]

    def __init__(self, compileParams, parentNode):
        super().__init__(compileParams, parentNode)


class TopPanel(Menu):
    height    = 30
    bg        = "cornflowerblue"
    row       = 0
    column    = 10
    label     = None

    def __init__(self, compileParams, parentNode):
        self.width     = parentNode.width
        #self.listeners = []

        super().__init__(compileParams, parentNode)


BASIC_TYPES = {
    "MainFrame": MainFrame,
    "TopPanel":  TopPanel
}