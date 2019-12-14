from sys import path as sys_path


if __name__ == "__main__":
    sys_path.append("bin")
    
    from bin import Engine
    from gui import MainFrame

    Engine(MainFrame).run()