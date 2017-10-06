import arcade
from random import randint
from pyglet.window import key

win_w = 800
win_h = 600
sp = 5
keys = key.KeyStateHandler()

class Star:
    def __init__(self,x,y,sp):
        self.x = x
        self.y = y
        self.sp = sp
        self.Star = arcade.Sprite('images/star.png')
        self.Star.set_position(self.x,self.y)
        
    def draw(self):
        self.Star.draw()

#    def fire(self):
#        starbullet = StarBullet(self.x,self.y+10)
#        starbullet.draw()    

    def move(self):
        if (self.x == win_w-50 or self.x == 50):
            self.sp = -self.sp
            self.x += self.sp
        else:
            self.x += self.sp
            self.Star.set_position(self.x,self.y)

class StarBullet:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.Star_bul = arcade.Sprite('images/star_bullet.png')
        self.Star_bul.set_position(self.x,self.y)
        
    def draw(self):
        self.Star_bul.draw()
        self.move()

    def move(self):
        self.y -= 5
        self.Star_bul.set_position(self.x,self.y)

class SealBullet:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.Seal_bul = arcade.Sprite('images/seal_bullet.png')
        self.Seal_bul.set_position(self.x,self.y)
        
    def draw(self):
        self.Seal_bul.draw()
        self.move()

    def move(self):
        self.y += 10
        self.Seal_bul.set_position(self.x,self.y)
            
class Player:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.Seal = arcade.Sprite('images/seal.png')
        self.Seal.set_position(self.x,self.y)

    def draw(self):
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

    def fire(self,keys):
        if keys[key.SPACE]:
            return True
        else:
            return False
        
            
player = Player(400,100)
star = Star(400,500,sp)
starbullet = StarBullet(star.x,star.y)
sealbullets = []

def on_draw(delta_time):
    arcade.start_render()
    star.draw()
    player.draw()
    star.move()
    player.move(keys)
    for sealbullet in sealbullets:
        sealbullet.draw()
    if (player.fire(keys) == True):
        sealbullets.append(SealBullet(player.x,player.y))
    #starbullet.draw()
    
def main():
    arcade.open_window(win_w,win_h,"SPACE SEAL")
    arcade.set_background_color(arcade.color.BLACK)
    arcade.get_window().push_handlers(keys)
    arcade.schedule(on_draw,1/80)
    arcade.run()

if __name__ == '__main__':
    main()
