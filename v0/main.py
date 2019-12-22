from time import sleep
from bearlibterminal import terminal as blt

from graphics.window import GameWindow

def main():

    # initialize stuff
    blt.open()
    
    # Initialize game window
    win = GameWindow(blt)
    
    # Initialize input methods
    blt.set("input.filter={keyboard, mouse+}")

    _dest = None
    # main game loop is here
    while True:
        # animations,loops etc
        mx = blt.state(blt.TK_MOUSE_X)
        my = blt.state(blt.TK_MOUSE_Y)
        
        # process input here
        # inputhandler = InputHandler() or something
        # inputhandler.read, etc
        if blt.has_input():
            key = blt.read()
            
            if key == blt.TK_CLOSE or key == blt.TK_ESCAPE:
                blt.close()
                break
            elif key == blt.TK_R:
                # rerun mapgen
                win.reset_digger()
            elif key == blt.TK_MOUSE_LEFT:
                _dest = (mx, my)
            elif key == blt.TK_MOUSE_RIGHT:
                _dest = None

        win.show_map_dists(mx,my)
        if _dest:
            win.draw_path(_dest, (mx,my))

        # blt.color(blt.color_from_name('blue'))
        # blt.put(mx, my, 0x2588)

        win.update()
        
if __name__ == '__main__':
    main()
