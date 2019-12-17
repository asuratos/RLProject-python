from mapgen.dig import Digger

class GameWindow:
    def __init__(self, blt):
        self.blt = blt
        
        mapwidth = 70
        mapheight = 30

        self.set_digger(mapwidth, mapheight, 'default', False)
        
        self.set_title(f'window: size={mapwidth + 20}x{mapheight}, title=RLTest;')
        
        # right now, prints are done with coords relative to the whole window.
        # should be changed to a set of panels, and prints are assigned relative to 
        # each panel's position (panel1(0,0) is different from panel2(0,0), etc.)
        
        self.blt.printf(0, 0, str(self.floor))
        self.blt.printf(mapwidth+1, 15, 'Side pane here!')
        
        # Initial refresh
        self.blt.refresh()

        # print(a.roomgraph)
    
    def update(self):
        # update each panel (subwindow) contents
        
        # refresh
        self.blt.refresh()
        
    def set_title(self, fstr):
        self.blt.set(fstr)
    
    def set_digger(self, mapwidth, mapheight, floortype = 'default', letters = False, room_attempts = 75):
        self.floor = Digger(mapwidth, mapheight, letters, floortype)
        self.floor.dig_floor(room_attempts)
        
    def reset_digger(self, room_attempts = 75):
        self.floor.reset()
        self.floor.dig_floor(room_attempts)
