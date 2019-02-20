
from pythonosc import dispatcher
from pythonosc import osc_server
import pygame
import numpy as np
import argparse
import sys

class KaraokeGame:
    def __init__(self, max_history=20, canvas_size=(800, 300), padding=50, players=[]):
        self.canvas_size = canvas_size
        self.min_y_pos = padding
        self.y_range = canvas_size[1] - (2 * padding)
        self.players = players
        
        self.song = [np.abs(np.sin(i)) for i in np.linspace(-np.pi, 40*np.pi, 8000)]
        # Place a red bar every 500 notes
        for i in range(0, len(self.song)):
            if (i % 500 == 0):
                self.song[i] = -1
        self.time = 0
        self.scores = []
        
        # Define max histoy size and initialize default (empty) history.
        self.max_history = max_history
        self.history = []
        
        # Define color hex.
        #self.colors = {'black': (0,0,0),
        #               'white': (255,255,255),
        #               'red': (255,0, 0),
        #               'green': (0,255,0),
        #               'blue': (0,0,255)}
        
        # Define player colors.
        #self.player_colors = {1: 'white',
        #                     2: 'green',
        #                     3: 'blue',
        #                     4: 'red'} 
        
        self.current_player = players[0]
        
        # Initialize pygame
        pygame.init()
        
        # Initialize pygame font module (used to display text)
        pygame.font.init()
        self.myfont = pygame.font.SysFont('Comic Sans MS', 30)
        
        # Initialize white game canvas
        self.game_canvas = pygame.display.set_mode(canvas_size)
        self.game_canvas.fill((255,255,255))
        
        pygame.display.set_caption('Hello World!')     


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
        y_pos = self.canvas_size[1] - (int(y * self.y_range) + self.min_y_pos)
        return(y_pos)

    def calc_score(self, y, y_hat):
        # Calculate score as difference of y and y_hat.
        # Append score to self.scores, and return score for display.
        #if ((note < 0) and (self.current_player is not self.players[0])):
        if (y < 0) and (self.current_player is not self.players[0]):
            self.score = -100 * (len(self.current_player.scores)/2)
            self.current_player.scores = self.current_player.scores + [self.score]
            return(self.score)
        else:
            self.score = 100 - (int(np.abs(y - y_hat) * 100))
            self.current_player.scores = self.current_player.scores + [self.score]
            return(self.score)


    def display_score(self, score):
        textsurface = self.myfont.render('{}'.format(score), False, (0, 155, 155))
        textsurface_score_1 = self.myfont.render('Score: {}'.format(int(np.mean(self.players[1].scores))), False, (0, 255, 0))
        #textsurface_total_2 = self.myfont.render('Score: {}'.format(int(np.mean(self.players[2].scores))), False, (0, 0, 255))
        #textsurface_total_3 = self.myfont.render('Score: {}'.format(int(np.mean(self.players[3].scores))), False, (255, 0, 0))
        self.game_canvas.blit(textsurface,(0,0))
        self.game_canvas.blit(textsurface_score_1,(0,250))
        #self.game_canvas.blit(textsurface_total_2,(0,210))
        #self.game_canvas.blit(textsurface_total_3,(0,250))


    def update_display(self, signal_name, y):
        # Check if game window has been closed. 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        y_avg = self.update_history(y)
        
        # only use every 5 updates because we get updates too frequently
        if self.time % 5 != 0:
            self.time += 1
            return
        
        self.game_canvas.fill((255,255,255))
        
        for note_index in range(self.time, (self.time + self.canvas_size[0])):
            try:
                note = self.song[note_index]
            except:
                note = 0
                
            if(note > 0):
                pygame.draw.circle(self.game_canvas, 
                                   (0,0,0),
                                   (50 + (note_index - self.time), self.calc_y_pos(note)),
                                   30,
                                   0)
            if(note < 0):
                r = pygame.Rect(50 + (note_index - self.time), 0, 30, self.canvas_size[1])
                pygame.draw.rect(self.game_canvas, (255,0,0), r)
        
        # If y_avg > 0, update display using y_avg to calculate the y-position 
        # of the feedback circle.
        if y_avg > 0:
            y_pos = self.calc_y_pos(y_avg)
            # Circle color is the color mapped to the given player stored in 
            # current_player.
            circle_color = self.current_player.color
                
            pygame.draw.circle(self.game_canvas,
                               circle_color,
                               (50, y_pos), 
                               20, 
                               0)
                
            
        score = self.calc_score(self.song[self.time], y_avg)
        self.display_score(score) 
        
        self.time += 1
        pygame.display.update()
            
        
    def singer_handler(self, signal_name, singer):
        self.current_player = self.players[int(singer-1)]
         
         
class Player:
    def __init__(self, color=(0,0,0), scores=[0], name="Somebody"):
        self.color = color
        self.scores = scores
        self.name = name
    
    
if __name__ == "__main__":
    p0 = Player(color=(255,255,255), name="Nobody")
    p1 = Player(color=(0,255,0))
    singers = [p0,p1]
    game = KaraokeGame(players=singers)
    
    # Parse arguments for host ip and port.
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
        default='127.0.0.1', help="The ip to listen on")
    parser.add_argument("--port",
        type=int, default='12000', help="The port to listen on")
    args = parser.parse_args()
    
    # Create dispatcher to handle incoming OSC messages.
    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("/wek/update", game.update_display)
    dispatcher.map("/wek/singer", game.singer_handler)
    
    server = osc_server.ThreadingOSCUDPServer(
            (args.ip, args.port), dispatcher)
        
    print("Serving on {}".format(server.server_address))
    server.serve_forever()

