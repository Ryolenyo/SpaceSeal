import arcade
from random import randint
from pyglet.window import key

win_w = 800
win_h = 600
keys = key.KeyStateHandler()

class Player:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.Seal = arcade.Sprite('images/seal.png')
        self.Seal.set_position(self.x,self.y)

    def draw(self):
        arcade.start_render()
        self.Seal.draw()

    def move(self,keys):
        if keys[key.LEFT]:
            self.x -= 3
            self.Seal.set_position(self.x,self.y)
        if keys[key.RIGHT]:
            self.x += 3
            self.Seal.set_position(self.x,self.y)
        if keys[key.UP]:
            self.y += 3
            self.Seal.set_position(self.x,self.y)
        if keys[key.DOWN]:
            self.y -= 3
            self.Seal.set_position(self.x,self.y)
        
            
player = Player(400,100)       
        

def on_draw(delta_time):
    arcade.start_render()
    player.move(keys)
    player.draw()
    
    
def main():
    arcade.open_window(win_w,win_h,"SPACE SEAL")
    arcade.set_background_color(arcade.color.BLACK)
    arcade.get_window().push_handlers(keys)
    arcade.schedule(on_draw,1/80)
    arcade.run()

if __name__ == '__main__':
    main()
