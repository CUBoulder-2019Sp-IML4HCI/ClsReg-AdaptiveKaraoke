from pythonosc import dispatcher
from pythonosc import osc_server
import pygame
import numpy as np
import argparse

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0, 0)
GREEN = (0,255,0)
BLUE = (0,0,255)
    
pygame.init()
history = []
singerColor = BLACK
singerDict = {
        1:WHITE,
        2:GREEN,
        3:BLUE,
        4:BLACK
        }

def update_display(x,y):
    print(x,y)
    if len(history) < 25:
        history.append(y)
        y_avg = np.mode(history)
        
    elif y > 0.1:
        history.append(y)
        history.pop(0)
        y_avg = np.mean(history)
    else:
        y_avg = 0
        
    if y_avg > 0:
        DISPLAYSURF.fill(WHITE)
        pygame.draw.circle(DISPLAYSURF, singerColor, (50, 300-(int(y_avg*200)+50)), 20, 0)
        pygame.display.update()
    else:
        DISPLAYSURF.fill(WHITE)
        pygame.display.update()

def singer_handler(x, singer):
    global singerColor
    singerColor = singerDict[singer]
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
        default="127.0.0.1", help="The ip to listen on")
    parser.add_argument("--port",
        type=int, default=12000, help="The port to listen on")
    args = parser.parse_args()

    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("/wek/update", update_display)
    dispatcher.map("/wek/singer", singer_handler)
    
    DISPLAYSURF = pygame.display.set_mode((800, 300))
    DISPLAYSURF.fill(WHITE)
    pygame.draw.circle(DISPLAYSURF, BLUE, (50, 50), 20, 0)
    pygame.display.set_caption('Hello World!')     
    server = osc_server.ThreadingOSCUDPServer(
        (args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()

