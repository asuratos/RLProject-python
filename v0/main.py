from graphics.window import GameWindow

def main():

    # initialize stuff
    a = GameWindow()

    # main game loop is here
    while True:
        
        if a.blt.has_input():
            key = a.blt.read()
            
            # process input here
            if key == a.blt.TK_CLOSE or a.blt.TK_ESC:
                a.blt.close()
                break
                
if __name__ == '__main__':
    main()
