from mapgen.dig import Digger

class GameWindow:
    def __init__(self, blt):
        self.blt = blt
        
        mapwidth = 70
        mapheight = 30

        self.set_digger(mapwidth, mapheight, 'default', False)
        
        self.blt.color(
        self.set_title(f'window: size={mapwidth + 20}x{mapheight}, title=RLTest;')
        
        # right now, prints are done with coords relative to the whole window.
        # should be changed to a set of panels, and prints are assigned relative to 
        # each panel's position (panel1(0,0) is different from panel2(0,0), etc.)
        
        self.show_map()
        
        # show side pane        
        self.blt.color(self.blt.color_from_name('white'))
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
        
    def show_map(self):
        _rooms = self.floor.roomcount

        self.blt.bkcolor(self.blt.color_from_name('brown')) #doorbg
        self.blt.color(self.blt.color_from_name('black'))   #doorfg
        # put doors
        for pt in self.floor.doors:
            self.blt.put(pt[0], pt[1], '+')
        
        for x in range(self.floor.width):
            for y in range(self.floor.height):
                # get element
                _tile = self.floor[x,y]
                if tile != 0:
                    _color = 55 + ((_tile/_rooms)*200)
                else:
                    _color = 0
                    
                self.blt.bkcolor(self.blt.color_from_argb(f'{_color},{_color},{_color}'))
                self.blt.put(x,y,' ')
                pass
        
        # naive print
        # self.blt.printf(0, 0, str(self.floor))
