
from pythonosc import dispatcher
from pythonosc import osc_server
import pygame
import numpy as np
import argparse

class KareokeGame:
    def __init__(self, ip='127.0.0.1', port='12000', max_history=20, canvas_size=(800, 300), padding=50):
        parser = argparse.ArgumentParser()
        parser.add_argument("--ip",
            default=ip, help="The ip to listen on")
        parser.add_argument("--port",
            type=int, default=port, help="The port to listen on")
        args = parser.parse_args()
        
        self.canvas_size = canvas_size
        self.min_y_pos = padding
        self.y_range = canvas_size[1] - (2 * padding)
        
        #proto_song = [np.abs(np.sin(i)) for i in range(0, 100, 0.1)]
        self.song = [np.abs(np.sin(i)) for i in np.linspace(-np.pi, 10*np.pi, 2000)]
        self.codify_song()
        self.time = 0
        
        # Define max histoy size and initialize default (empty) history.
        self.max_history = max_history
        self.history = []
        
        # Define color hex.
        self.colors = {'black': (0,0,0),
                       'white': (255,255,255),
                       'red': (255,0, 0),
                       'green': (0,255,0),
                       'blue': (0,0,255)}
        
        # Define player colors.
        self.player_colors = {1: 'white',
                             2: 'green',
                             3: 'blue',
                             4: 'red'} 
        
        self.current_player = 4
        
        # Create dispatcher to handle incoming OSC messages.
        self.dispatcher = dispatcher.Dispatcher()
        self.dispatcher.map("/wek/update", self.update_display)
        self.dispatcher.map("/wek/singer", self.singer_handler)
        
        # Initialize white game canvas
        self.game_canvas = pygame.display.set_mode(canvas_size)
        self.game_canvas.fill(self.colors['white'])
        
        #pygame.draw.circle(self.game_canvas, self.colors['white'], (50, 50), 20, 0)
        pygame.display.set_caption('Hello World!')     
        
        self.server = osc_server.ThreadingOSCUDPServer(
            (args.ip, args.port), self.dispatcher)
        
        print("Serving on {}".format(self.server.server_address))
        self.server.serve_forever()
   
    def update_history(self, y):
        # If the len(history) < max_history, append y to history and take mean.
        # Do not pop from history until history has reach max history size.
        if len(self.history) < self.max_history:
            self.history.append(y)
            y_avg = np.mean(self.history)
            
        # If len(history) == max_history, append y to end of history, pop
        # first element of history, and take mean.
        elif y > 0.1:
            self.history.append(y)
            self.history.pop(0)
            y_avg = np.mean(self.history)
        
        # If y < 0.1, do not change history. Use 0 for y_avg.
        else:
            y_avg = 0
        
        return(y_avg)
        
        
    def calc_y_pos(self, y):
        # The range of y is defined as the y dimension of the canvas - 
        # 2 * padding.
        # y_pos is found by scaling y_range with y_avg, and then adding the
        # minimum y position (the padding).
        y_pos = int(y * self.y_range) + self.min_y_pos
        return(y_pos)

        
    def codify_song(self):
        for continuous_val in self.song[:]:
            continuous_val = self.calc_y_pos(continuous_val)


    def update_display(self, signal_name, y):
        y_avg = self.update_history(y)
        
        if self.time % 5 != 0:
            self.time += 1
            return
        
        self.game_canvas.fill(self.colors['white'])
        
        for note_index in range(self.time, self.canvas_size[0]):
            try:
                note = self.song[note_index]
            except:
                note = 0
                
            if(note != 0):
                pygame.draw.circle(self.game_canvas, 
                                   self.colors['black'],
                                   (50 + (note_index - self.time), self.calc_y_pos(note)),
                                   30,
                                   0)
        self.time += 1
        
        # If y_avg > 0, update display using y_avg to calculate the y-position 
        # of the feedback circle.
        if y_avg > 0:
            y_pos = self.calc_y_pos(y_avg)
            # Circle color is the color mapped to the given player stored in 
            # current_player.
            circle_color = self.colors[self.player_colors[self.current_player]]
                
            pygame.draw.circle(self.game_canvas,
                               circle_color,
                               (50, y_pos), 
                               20, 
                               0)
        
        pygame.display.update()
            
        
    def singer_handler(self, signal_name, singer):
         self.current_player = singer
    
if __name__ == "__main__":
    game = KareokeGame()

