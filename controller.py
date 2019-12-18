from bin.basic_types import Controller


class MENU(Controller):
    
    def left_click(trigger, event):
        print(event, trigger)