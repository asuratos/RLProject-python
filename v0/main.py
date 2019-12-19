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

        win.show_map()

        blt.color(blt.color_from_name('blue'))
        blt.put(mx, my, 0x2588)

        win.update()
        
if __name__ == '__main__':
    main()
