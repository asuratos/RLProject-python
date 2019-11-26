from bearlibterminal import terminal
from mapgen.dig import Digger

mapwidth = 70
mapheight = 30

a = Digger(mapwidth, mapheight)
a.dig_floor(30)

terminal.open()
terminal.set(f'window: size={mapwidth + 20}x{mapheight}, title=RLTest;')
terminal.printf(0, 0, str(a))
terminal.printf(mapwidth+1, 15, 'Side pane here!')
terminal.refresh()
 
while terminal.read() != terminal.TK_CLOSE:
    pass
 
terminal.close()
