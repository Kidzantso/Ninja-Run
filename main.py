from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.properties import NumericProperty
from kivy.clock import Clock
from kivy.core.window import Window
import random
import math

class Ninja(Widget):
    velocity_y = NumericProperty(0)
    gravity = -1
    jump_strength = 15

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.image = Image(source='assets/ninja.png', size=(70, 70), pos=self.pos)
        self.add_widget(self.image)
    
    def jump(self):
        if self.y <= 100:
            self.velocity_y = self.jump_strength
    
    def update(self):
        self.velocity_y += self.gravity
        self.y += self.velocity_y
        
        if self.y < 100:
            self.y = 100
            self.velocity_y = 0
        
        self.image.pos = self.pos
    
    def collides_with(self, obstacle):
        # Circle-to-rectangle collision detection
        ninja_center = (self.center_x, self.center_y)
        obstacle_center = (obstacle.center_x, obstacle.center_y)
        # Calculate distance between the centers of the ninja and the obstacle
        distance = math.sqrt((ninja_center[0] - obstacle_center[0]) ** 2 + 
                             (ninja_center[1] - obstacle_center[1]) ** 2)
        # Using the sum of radii for collision detection (approximated as circle vs box)
        ninja_radius = self.width / 2
        obstacle_radius = obstacle.width / 2
        return distance < (ninja_radius + obstacle_radius)

class Obstacle(Widget):
    def __init__(self, speed, **kwargs):
        super().__init__(**kwargs)
        self.speed = speed
        self.image = Image(source='assets/obstacle.png', size=self.size, pos=self.pos)
        self.add_widget(self.image)
    
    def update(self):
        self.x -= self.speed
        self.image.pos = self.pos


class Game(Widget):
    score = NumericProperty(0)
    high_score = NumericProperty(0)  # Track the highest score during the session
    obstacle_speed = NumericProperty(5)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bg = Image(source='assets/background.png', allow_stretch=True, keep_ratio=False, size=Window.size, pos=(0, 0))
        self.add_widget(self.bg)
        
        self.ninja = Ninja(pos=(50, 120), size=(70, 70))
        self.add_widget(self.ninja)
        
        self.obstacles = []
        self.game_over_label = Label(text="", font_size=40, pos=(Window.width / 2, Window.height / 2))
        self.add_widget(self.game_over_label)
        
        self.score_label = Label(text=f"Score: {self.score}", font_size=30, pos=(20, Window.height - 90))
        self.add_widget(self.score_label)
        
        self.restart_button = Button(text="Restart", size_hint=(None, None), size=(200, 50),
                                     pos=(Window.width / 2 - 50, Window.height / 2 - 70))
        self.restart_button.bind(on_press=self.restart_game)
        self.restart_button.opacity = 0
        self.restart_button.disabled = True
        self.add_widget(self.restart_button)
        
        self.start_game()
    
    def start_game(self):
        self.ninja.pos = (50, 120)
        self.ninja.velocity_y = 0
        self.score = 0
        self.obstacle_speed = 5
        
        for obstacle in self.obstacles:
            self.remove_widget(obstacle)
        self.obstacles.clear()
        
        self.game_over_label.text = ""
        self.restart_button.opacity = 0
        self.restart_button.disabled = True
        
        Clock.schedule_interval(self.spawn_obstacle, 2.0)
        Clock.schedule_interval(self.update, 1/60)
    
    def spawn_obstacle(self, dt):
        if len(self.obstacles) < 2:
            gap = random.randint(150, 250)
            obstacle1 = Obstacle(self.obstacle_speed, pos=(Window.width, 100), size=(40, 40))
            obstacle2 = Obstacle(self.obstacle_speed, pos=(Window.width + gap, 100), size=(40, 40))
            
            self.obstacles.append(obstacle1)
            self.obstacles.append(obstacle2)
            
            self.add_widget(obstacle1)
            self.add_widget(obstacle2)
    
    def update(self, dt):
        self.ninja.update()
        self.score += 1
        self.score_label.text = f"Score: {self.score}"
        
        if self.score % 100 == 0:
            self.obstacle_speed += 0.5
        
        for obstacle in self.obstacles[:]:
            obstacle.speed = self.obstacle_speed
            obstacle.update()
            if self.ninja.collides_with(obstacle):
                self.game_over()
            if obstacle.x < -40:
                self.remove_widget(obstacle)
                self.obstacles.remove(obstacle)
    
    def game_over(self):
        # Update high score if the current score is higher
        if self.score > self.high_score:
            self.high_score = self.score
        
        Clock.unschedule(self.update)
        Clock.unschedule(self.spawn_obstacle)
        self.game_over_label.text = f"Game Over!\nScore: {self.score}\nHigh Score: {self.high_score}"  # Display score and high score at game over
        self.restart_button.opacity = 1
        self.restart_button.disabled = False
    
    def restart_game(self, instance):
        self.clear_widgets()
        self.__init__()

    def on_touch_down(self, touch):
        if self.restart_button.collide_point(*touch.pos):
            return super(Game, self).on_touch_down(touch)
        self.ninja.jump()


class NinjaRunApp(App):
    def build(self):
        return Game()


if __name__ == "__main__":
    NinjaRunApp().run()
