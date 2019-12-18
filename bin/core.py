from bin.basic_types import BASIC_TYPES


class Compiler:
    compiled        = []
    controllers     = None
    _ignoredParamse = [
        '__module__',
        '__dict__'
    ]

    def compileElement(self, decl, parentNode=None, render=True):
        prototype       = BASIC_TYPES[decl["cls"]]
        compileParams   = self._getCompileParamsByClass(prototype, decl)
        examplar        = prototype(compileParams, parentNode=parentNode)
        examplar.dom    = self._generateDom(examplar)
        
        self.compiled.append(examplar)

        if examplar.items:      self.compile_elements(examplar.items, examplar, render)
        if examplar.controller: self.connect_controlles(examplar)

        return examplar

    def connect_controlles(self, examplar):
        if examplar.controller in self.controllers:
            examplar.setController(self.controllers[examplar.controller])
        else:
            raise KeyError("Key: {0} not found in controllers diction.".format(examplar.controller))

    def compile_elements(self, items, parentNode=None, render=True):
        for item in items:
            self.compileElement(item, parentNode, render)

    def _generateDom(self, prototype):
        if prototype.packParams:
            return prototype.tk_type(
                master=prototype.parentNode.dom if prototype.parentNode else None, 
                **prototype.getPackParams()
            )
        else:
            return prototype.tk_type()

    def _getCompileParamsByClass(self, prototype, decl):
        params  = {}
        ignored = prototype.ignored + self._ignoredParamse if "ignored" in prototype.__dict__ else self._ignoredParamse

        return {k: decl[k]
            for k,v in decl.items()
            if hasattr(prototype, k) and not k in ignored
        }


class Engine(Compiler):

    def __init__(self, config, controllers):
        self.config        = config
        self.controllers   = controllers
        self.config["cls"] = 'MainFrame'
        self.mainFrame     = self.compileElement(self.config, render=False)

    def mainloop(self):
        for el in self.compiled:
            if el != self.mainFrame: el.render()

        self.mainFrame.render()