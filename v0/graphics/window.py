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
        
        self.show_map()
        
        # show side pane        
        self.blt.color(self.blt.color_from_name('white'))
        self.blt.bkcolor(self.blt.color_from_name('black'))
        self.blt.printf(mapwidth+1, 3, 'Placeholder:')

        # self.blt.bkcolor(self.blt.color_from_name('red'))
        self.blt.printf(mapwidth+1, 4, 'HP:[bkcolor=red]          ')
        self.blt.printf(mapwidth+1, 5, 'SP:[bkcolor=blue]          ')
        
        
        self.blt.printf(mapwidth+1, 7, 'Ikjashdr')
        self.blt.printf(mapwidth+1, 8, 'adkjvnut')
        
        # Initial refresh
        self.blt.refresh()

        # print(a.roomgraph)
    
    def check_mouse_onfloor(self, x, y):
        return (x,y) in self.floor.floorgraph
    
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
        
        for x in range(self.floor.width):
            for y in range(self.floor.height):
                # get element
                _tile = self.floor.floor[x,y]
                if _tile != 0:
                    _color = 100 + int((_tile/_rooms)*155)
                    self.blt.bkcolor(self.blt.color_from_argb(255,255,255-_color,255-_color))
                else:
                    _color = 0
                    self.blt.bkcolor(self.blt.color_from_name('black'))
                    
                self.blt.print(x,y,' ')
                pass
        
        # put doors
        self.blt.bkcolor(self.blt.color_from_name('orange')) #doorbg
        self.blt.color(self.blt.color_from_name('black'))   #doorfg
        for pt in self.floor.doors:
            self.blt.print(pt[0], pt[1], '+')
        # naive print
        # self.blt.printf(0, 0, str(self.floor))

    def show_map_dists(self, mx, my):
        _rooms = self.floor.roomcount
        _dists = self.floor.floorgraph.get_dists((mx,my))
        
        for x in range(self.floor.width):
            for y in range(self.floor.height):
                # get element
                _tile = self.floor.floor[x,y]
                
                if (x, y) in _dists:
                    _dist = _dists[(x,y)] * 7 
                    if _dist > 200:
                        _dist = 200
                    self.blt.bkcolor(self.blt.color_from_argb(255,255-_dist,255-_dist,255-_dist))
                else:
                    _color = 0
                    self.blt.bkcolor(self.blt.color_from_name('black'))
                    
                self.blt.print(x,y,' ')
                pass
        
        # put doors
        self.blt.bkcolor(self.blt.color_from_name('orange')) #doorbg
        self.blt.color(self.blt.color_from_name('black'))   #doorfg
        for pt in self.floor.doors:
            self.blt.print(pt[0], pt[1], '+')
        # naive print
        # self.blt.printf(0, 0, str(self.floor))
    
    def draw_path(self, pt1, pt2):
        self.blt.composition(self.blt.TK_ON)

        path = self.floor.floorgraph.get_path(pt1, pt2)

        self.blt.bkcolor(self.blt.color_from_argb(0,0,0,0))
        self.blt.color(self.blt.color_from_name('blue'))
        self.blt.print(*pt1, '*')
        current = pt2
        while current != pt1:
            self.blt.print(*current, '*')
            current = path[current]

        self.blt.composition(self.blt.TK_OFF)