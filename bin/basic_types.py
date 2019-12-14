import tkinter
import ctypes
import platform


MENU_ELEMENTS = ["TopPanel"]


class Window:
    
    @staticmethod
    def _getSizeWindows():
        user32 = ctypes.windll.user32
        
        return {
            "width":  user32.GetSystemMetrics(0), 
            "height": user32.GetSystemMetrics(1)
        }
    
    @staticmethod
    def _getSizeUNIX():
        root = tkinter.Tk()
        
        return {
            "width":  root.winfo_screenwidth(), 
            "height": root.winfo_screenheight()
        }
    
    @staticmethod
    def getSize():
        if (platform.system() == 'Windows'):
            return Window._getSizeWindows()
        else:
            return Window._getSizeUNIX()


    @staticmethod
    def getWidth():
        return Window.getSize()["width"]

    @staticmethod
    def getHeight():
        return Window.getSize()["height"]


class EventListener:

    def __init__(self, event, action):
        self.event  = event
        self.action = action


class BasicElement:
    compileParams = {}
    parentNode    = None
    packParams    = {}
    listeners     = [{}]
    children      = []
    items         = []
    dom           = None
    tag           = None

    def __init__(self, parentNode):
        self.parentNode = parentNode
    
    def addEventListener(self, event, action):
        self.dom.bind(event, action)

    def appendChild(self, child):
        child.parentNode = self

        self.children.append(child)
        child.pack()

    def _compile(self):
        if (self.parentNode):
            self.dom = self.tag(master=self.parentNode.dom, **self.compileParams)
        else:
            self.dom = self.tag(**self.compileParams)

        self._compile = None

    def pack(self):
        self.dom.pack(**self.packParams)


class MainFrame(BasicElement):
    tag           = tkinter.Frame
    panel         = None
    wizards       = []
    compileParams = {
        "width":  Window.getWidth(), 
        "height": Window.getHeight()
    }

    def __init__(self, parentNode):
        self.items = [self.panel] if self.panel.__name__ in MENU_ELEMENTS else []

        super().__init__(parentNode)


class TopPanel(BasicElement):
    tag           = tkinter.Frame
    compileParams = {
        "bg":     "#ff5733",
        "width":  Window.getWidth(), 
        "height": 40
    }