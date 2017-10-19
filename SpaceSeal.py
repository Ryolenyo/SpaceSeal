import arcade
import random
import math
from random import randint

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class SealHP(arcade.Sprite):
    def __init__(self,file):
        super().__init__(file)

    def update(self):
        self.center_x += 0
        
        

class SealBullet(arcade.Sprite):
    def __init__(self,file):
        super().__init__(file)
        self.speed = 10

    def update(self):
        self.center_y += self.speed
        if (self.center_y == 600):
            self.kill()   

class StarBullet(arcade.Sprite):
    def __init__(self,file):
        super().__init__(file)
        self.speed = 5

    def update(self):
        self.center_y -= self.speed
        

class SealSprite(arcade.Sprite):
    def __init__(self,file):
        super().__init__(file)
        self.life = 5
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

class StarSprite(arcade.Sprite):
    def __init__(self,file):
        super().__init__(file)
        self.speed = 5
        self.life = 50

    def update(self):
        self.center_x += self.speed
        if self.center_x > 600 or self.center_x < 200:
            self.speed = -self.speed

        

class MyWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH,SCREEN_HEIGHT)
        self.all_sprites_list = None
        self.bullet_list = None
        self.enemy_bullet_list = None
        self.player_sprite = None

    def start_new_game(self):
        self.all_sprites_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
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

    def on_draw(self):
        arcade.start_render()

        minutes = int(self.total_time)//60
        seconds = int(self.total_time)%60

        output = f"Time: {minutes:02d}:{seconds:02d}"

        if not self.timer_text or self.timer_text.text != output:
            self.timer_text = arcade.create_text(output, arcade.color.WHITE, 10)

        arcade.render_text(self.timer_text, 700, 560)

        self.all_sprites_list.draw()
        self.player_sprite.update()
        self.enemy_sprite.update()
    

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

    def enemy_shoot(self,sec):
        if sec > self.count+0.5: #delay shooting 
            enemy_bullet_sprite = StarBullet("images/star_bullet.png")
            enemy_bullet_sprite.center_x = self.enemy_sprite.center_x
            enemy_bullet_sprite.center_y = self.enemy_sprite.center_y
            enemy_bullet_sprite.update()
            self.all_sprites_list.append(enemy_bullet_sprite)
            self.enemy_bullet_list.append(enemy_bullet_sprite)
            self.count += 1
        

def main():
        window = MyWindow()
        window.start_new_game()  
        arcade.run()

if __name__ == "__main__":
        main()
        
