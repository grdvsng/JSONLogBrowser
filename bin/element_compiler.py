from basic_types import *


class Compiler:

    @staticmethod
    def createElement(prototype, parentNode=None):
        compiled = Compiler.compile_element(prototype, parentNode)

        if (parentNode):
            parentNode.appendChild(compiled)
        else:
            compiled.pack()

        if compiled.items: 
            Compiler.compile_children(compiled.items, compiled)

        return compiled

    @staticmethod
    def compile_children(children, master):
        for child in children:
            Compiler.createElement(child, master)

    @staticmethod
    def compile_element(prototype, parentNode=None):
        elem = prototype(parentNode)

        elem._compile()
        
        if (len(elem.listeners) > 0):
            Compiler.addEventListeners(elem, elem.listeners)

        return elem

    @staticmethod
    def addEventListeners(elem, listeners):
        for evListener in listeners:
            if isinstance(evListener, EventListener):
                elem.addEventListener(evListener.event, evListener.action)
