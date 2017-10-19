import arcade
import random
import math
from random import randint

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

'''--------------------------item-------------------------'''

class itemPower(arcade.Sprite):
    def __init__(self,file):
        super().__init__(file)
        self.speed = 20

    def update(self):
        self.center_y += self.speed
        self.center_x += self.speed
        if (self.center_y == 600 or self.center_y == 0 or self.center_x == 800 or self.center_x == 0):
            self.kill()
        

'''--------------------------player-------------------------'''

class SealHP(arcade.Sprite):
    def __init__(self,file):
        super().__init__(file)

    def update(self):
        self.center_x += 0
        

class SealBullet(arcade.Sprite):
    def __init__(self,file):
        super().__init__(file)
        self.speed = 20

    def update(self):
        self.center_y += self.speed
        if (self.center_y == 600):
            self.kill()

class SealSprite(arcade.Sprite):
    def __init__(self,file):
        super().__init__(file)
        self.life = 3
        self.speed_x = 0
        self.speed_y = 0

    def update(self):
        self.center_x += self.speed_x
        self.center_y += self.speed_y     

    def move(self,key):
        if key == arcade.key.LEFT:
            self.speed_x = -5
        if key == arcade.key.RIGHT:
            self.speed_x = 5
        if key == arcade.key.UP:
            self.speed_y = 5
        if key == arcade.key.DOWN:
            self.speed_y = -5

    def stop(self,key):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.speed_x = 0
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.speed_y = 0

    def hit(self,other,hit_size):
        return (abs(self.center_x - other.center_x) <= hit_size) and (abs(self.center_y - other.center_y) <= hit_size)


'''--------------------------enemy-------------------------'''

class StarBullet(arcade.Sprite):
    def __init__(self,file):
        super().__init__(file)
        self.speed = 5

    def update(self):
        self.center_y -= self.speed

class StarSprite(arcade.Sprite):
    def __init__(self,file):
        super().__init__(file)
        self.speed = 5
        self.life = 10

    def update(self):
        self.center_x += self.speed
        if self.center_x > 600 or self.center_x < 200:
            self.speed = -self.speed

    def hit(self,other,hit_size):
        return (abs(self.center_x - other.center_x) <= hit_size) and (abs(self.center_y - other.center_y) <= hit_size)

        
'''--------------------------window------------------------'''

over = False

class MyWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH,SCREEN_HEIGHT,over)
        self.all_sprites_list = None
        self.enemy_list = None
        self.bullet_list = None
        self.enemy_bullet_list = None
        self.player_sprite = None
        self.item_list = None

    def start_new_game(self):
        self.all_sprites_list = arcade.SpriteList()
        self.item_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.hp_list = arcade.SpriteList()
        self.enemy_bullet_list = arcade.SpriteList()
        self.player_sprite = SealSprite("images/seal.png")
        self.enemy_sprite = StarSprite("images/star.png")
        self.player_sprite.center_x = 400
        self.player_sprite.center_y = 100
        self.enemy_sprite.center_x = 400
        self.enemy_sprite.center_y = 500
        self.all_sprites_list.append(self.player_sprite)
        self.all_sprites_list.append(self.enemy_sprite)
        arcade.set_background_color(arcade.color.BLACK)

        self.total_time = 0.0
        self.timer_text = None
        self.count = 0

        #show HP
        for i in range(self.player_sprite.life):
            self.hp_sprite = SealHP("images/hp.png")
            self.hp_list.append(self.hp_sprite)
            self.all_sprites_list.append(self.hp_sprite)
            self.hp_sprite.center_x = 30 + i*30
            self.hp_sprite.center_y = 30
            self.hp_sprite.update()

    def on_draw(self):
        arcade.start_render()
        self.over = over

        minutes = int(self.total_time)//60
        seconds = int(self.total_time)%60

        output = f"Time: {minutes:02d}:{seconds:02d}"

        if not self.timer_text or self.timer_text.text != output:
            self.timer_text = arcade.create_text(output, arcade.color.WHITE, 10)

        arcade.render_text(self.timer_text, 700, 560)

        self.all_sprites_list.draw()
        self.player_sprite.update()
        self.enemy_sprite.update()

        if minutes == seconds :
            self.randomItem()

        self.item_list.update()

        
        #shoot player
        for bullet in self.enemy_bullet_list:
            if self.player_sprite.hit(bullet,20):
                bullet.kill()
                self.player_sprite.life -= 1
                self.hp_list[self.player_sprite.life].kill()
                #player die
                if self.player_sprite.life <=0:
                    self.player_sprite.kill()
                    self.over_sprite = OverSprite("images/youdied.png")
                    self.all_sprites_list.append(self.over_sprite)
                    self.over_sprite.center_x = 400
                    self.over_sprite.center_y = 300


                    
#                    self.over = True
#
#        if self.over == True: 
#            self.textover = "YOU DIED"
#            self.all_text = arcade.create_text(self.textover, arcade.color.WHITE, 30)
#            arcade.render_text(self.all_text, 400, 300)
    

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT or key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.move(key)
        if key == arcade.key.SPACE:
            bullet_sprite = SealBullet("images/seal_bullet.png")
            bullet_sprite.center_x = self.player_sprite.center_x
            bullet_sprite.center_y = self.player_sprite.center_y
            bullet_sprite.update()
            self.all_sprites_list.append(bullet_sprite)
            self.bullet_list.append(bullet_sprite)
            
    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT or key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.stop(key)

    def update(self,delta_time):
        self.total_time += delta_time
        self.enemy_shoot(int(self.total_time)%60)
        self.bullet_list.update()
        self.enemy_bullet_list.update()

        #shoot enemy
        for bullet in self.bullet_list:
            if self.enemy_sprite.hit(bullet,20):
                bullet.kill()
                self.enemy_sprite.life -= 1
                if self.enemy_sprite.life ==0:
                    self.enemy_sprite.kill()

    #random item position
    def randomItem(self):
        itempow_sprite = itemPower("images/powerup.png")
        itempow_sprite.center_x = randint(200,600)
        itempow_sprite.center_y = randint(150,450)
        itempow_sprite.update()
        self.all_sprites_list.append(itempow_sprite)
        self.item_list.append(itempow_sprite)
            
        
                

    def enemy_shoot(self,sec):
        stg1 = 1
        if sec > self.count: #delay shooting 
            enemy_bullet_sprite = StarBullet("images/star_bullet.png")
            enemy_bullet_sprite.center_x = self.enemy_sprite.center_x
            enemy_bullet_sprite.center_y = self.enemy_sprite.center_y
            enemy_bullet_sprite.update()
            self.all_sprites_list.append(enemy_bullet_sprite)
            self.enemy_bullet_list.append(enemy_bullet_sprite)
            self.count += stg1



class OverSprite(arcade.Sprite):
    def __init__(self,file):
        super().__init__(file)
        print("GAME OVER")

        
def main():
        window = MyWindow()
        window.start_new_game()  
        arcade.run()

if __name__ == "__main__":
        main()
        
