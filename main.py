import tkinter as tk
from tkinter import messagebox
import random
import os
from PIL import Image, ImageTk

class SnakeGame:
    def __init__(self, root, homescreen):
        self.root = root
        self.homescreen = homescreen
        self.root.title("Snake Game")
        self.root.configure(bg="black")
        
        for widget in self.root.winfo_children():
            widget.destroy()
            
        self.BOARD_WIDTH = 600
        self.BOARD_HEIGHT = 600
        self.UNIT_SIZE = 25
        self.GAME_SPEED = 120
        
        self.snake_body = [[100, 100]]
        self.direction = "right"
        self.score = 0
        self.game_running = True
        self.level = 1
        self.snake_color = "#00FF00"
        self.particles = []
        self.golden_apple_position = None
        self.golden_apple_timer = 0
        self.rainbow_effect = False
        self.rainbow_timer = 0
        
        self.food_position = self.create_food()
        
        self.canvas = tk.Canvas(
            self.root,
            bg="#1a1a1a",
            height=self.BOARD_HEIGHT,
            width=self.BOARD_WIDTH,
            highlightthickness=3,
            highlightbackground="#FFD700"
        )
        self.canvas.pack()
        
        self.load_images()
        
        self.create_ui()
        
        self.root.bind('<KeyPress>', self.change_direction)
        self.root.focus_set()
        
        if self.grass_photo:
            self.create_grass_background()
        self.draw_food()
        self.draw_golden_apple()
        self.draw_snake()
        self.update_ui()
        
        self.next_turn()
        
    def load_images(self):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            grass_path = os.path.join(current_dir, "grass.png")
            apple_path = os.path.join(current_dir, "apple.png")
            
            grass_img = Image.open(grass_path)
            grass_img = grass_img.resize((self.UNIT_SIZE, self.UNIT_SIZE), Image.Resampling.LANCZOS)
            self.grass_photo = ImageTk.PhotoImage(grass_img)
            
            apple_img = Image.open(apple_path)
            apple_img = apple_img.resize((self.UNIT_SIZE, self.UNIT_SIZE), Image.Resampling.LANCZOS)
            self.apple_photo = ImageTk.PhotoImage(apple_img)
            
            golden_apple_path = os.path.join(current_dir, "golden_apple.png")
            golden_apple_img = Image.open(golden_apple_path)
            golden_apple_img = golden_apple_img.resize((self.UNIT_SIZE, self.UNIT_SIZE), Image.Resampling.LANCZOS)
            self.golden_apple_photo = ImageTk.PhotoImage(golden_apple_img)
            
            self.create_grass_background()
            
        except Exception as e:
            print(f"Error loading images: {e}")
            self.grass_photo = None
            self.apple_photo = None
            self.golden_apple_photo = None
            
    def create_grass_background(self):
        if self.grass_photo:
            for x in range(0, self.BOARD_WIDTH, self.UNIT_SIZE):
                for y in range(0, self.BOARD_HEIGHT, self.UNIT_SIZE):
                    self.canvas.create_image(
                        x + self.UNIT_SIZE // 2,
                        y + self.UNIT_SIZE // 2,
                        image=self.grass_photo,
                        tags="background"
                    )
    
    def create_ui(self):
        ui_frame = tk.Frame(self.root, bg="black")
        ui_frame.pack(fill="x", padx=10, pady=5)
        
        self.score_label = tk.Label(
            ui_frame,
            text=f"Score: {self.score}",
            font=("Courier", 16, "bold"),
            fg="#00FF00",
            bg="black"
        )
        self.score_label.pack(side="left")
        
        self.level_label = tk.Label(
            ui_frame,
            text=f"Level: {self.level}",
            font=("Courier", 16, "bold"),
            fg="#FFD700",
            bg="black"
        )
        self.level_label.pack(side="left", padx=(20, 0))
        
        self.length_label = tk.Label(
            ui_frame,
            text=f"Length: {len(self.snake_body)}",
            font=("Courier", 16, "bold"),
            fg="#FF6B6B",
            bg="black"
        )
        self.length_label.pack(side="left", padx=(20, 0))
    
    def create_food(self):
        while True:
            x = random.randint(0, (self.BOARD_WIDTH // self.UNIT_SIZE) - 1) * self.UNIT_SIZE
            y = random.randint(0, (self.BOARD_HEIGHT // self.UNIT_SIZE) - 1) * self.UNIT_SIZE
            if [x, y] not in self.snake_body and (self.golden_apple_position is None or [x, y] != self.golden_apple_position):
                return [x, y]
    
    def create_golden_apple(self):
        while True:
            x = random.randint(0, (self.BOARD_WIDTH // self.UNIT_SIZE) - 1) * self.UNIT_SIZE
            y = random.randint(0, (self.BOARD_HEIGHT // self.UNIT_SIZE) - 1) * self.UNIT_SIZE
            if [x, y] not in self.snake_body and [x, y] != self.food_position:
                return [x, y]
    
    def update_golden_apple_spawn(self):
        self.golden_apple_timer += 1
        
        if self.golden_apple_position is None and self.golden_apple_timer > 100:
            if random.random() < 0.005:
                self.golden_apple_position = self.create_golden_apple()
                self.golden_apple_timer = 0
        
        elif self.golden_apple_position is not None:
            if self.golden_apple_timer > 250:
                self.golden_apple_position = None
                self.golden_apple_timer = 0
    
    def get_rainbow_color(self, offset=0):
        import math
        hue = (self.rainbow_timer + offset) * 0.1
        r = int((math.sin(hue) + 1) * 127.5)
        g = int((math.sin(hue + 2.094) + 1) * 127.5)
        b = int((math.sin(hue + 4.189) + 1) * 127.5)
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def check_collision(self, x, y):
        if x < 0 or x >= self.BOARD_WIDTH or y < 0 or y >= self.BOARD_HEIGHT:
            return True
        
        for body_part in self.snake_body:
            if x == body_part[0] and y == body_part[1]:
                return True
                
        return False
    
    def check_food(self):
        x, y = self.snake_body[0]
        
        if x == self.food_position[0] and y == self.food_position[1]:
            self.score += 10
            self.update_level()
            self.update_ui()
            self.create_eat_particles(x, y)
            self.food_position = self.create_food()
            return True
        
        if self.golden_apple_position and x == self.golden_apple_position[0] and y == self.golden_apple_position[1]:
            self.score += 50
            self.update_level()
            self.update_ui()
            self.create_golden_eat_particles(x, y)
            
            self.rainbow_effect = True
            self.rainbow_timer = 0
            
            self.golden_apple_position = None
            self.golden_apple_timer = 0
            
            self.snake_body.append(self.snake_body[-1].copy())
            return "golden"
        
        return False
    
    def update_level(self):
        new_level = (self.score // 50) + 1
        if new_level > self.level:
            self.level = new_level
            self.GAME_SPEED = max(80, 120 - (self.level * 5))
            colors = ["#00FF00", "#FFD700", "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7"]
            self.snake_color = colors[min(self.level - 1, len(colors) - 1)]
    
    def update_ui(self):
        self.score_label.config(text=f"Score: {self.score}")
        self.level_label.config(text=f"Level: {self.level}")
        self.length_label.config(text=f"Length: {len(self.snake_body)}")
    
    def create_eat_particles(self, x, y):
        for _ in range(8):
            particle = {
                'x': x + self.UNIT_SIZE // 2,
                'y': y + self.UNIT_SIZE // 2,
                'dx': random.randint(-3, 3),
                'dy': random.randint(-3, 3),
                'life': 15,
                'color': '#FFD700'
            }
            self.particles.append(particle)
    
    def create_golden_eat_particles(self, x, y):
        for _ in range(16):
            particle = {
                'x': x + self.UNIT_SIZE // 2,
                'y': y + self.UNIT_SIZE // 2,
                'dx': random.randint(-5, 5),
                'dy': random.randint(-5, 5),
                'life': 25,
                'color': random.choice(['#FFD700', '#FF6B00', '#FF1493', '#00CED1', '#ADFF2F'])
            }
            self.particles.append(particle)
    
    def update_particles(self):
        self.particles = [p for p in self.particles if p['life'] > 0]
        
        for particle in self.particles:
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            particle['life'] -= 1
            
            size = max(1, particle['life'] // 3)
            self.canvas.create_oval(
                particle['x'] - size, particle['y'] - size,
                particle['x'] + size, particle['y'] + size,
                fill=particle['color'], outline=""
            )
    
    def next_turn(self):
        if self.game_running:
            x, y = self.snake_body[0]
            
            if self.direction == "up":
                y -= self.UNIT_SIZE
            elif self.direction == "down":
                y += self.UNIT_SIZE
            elif self.direction == "left":
                x -= self.UNIT_SIZE
            elif self.direction == "right":
                x += self.UNIT_SIZE
            
            if self.check_collision(x, y):
                self.game_over()
                return
            
            self.snake_body.insert(0, [x, y])
            
            food_eaten = self.check_food()
            if food_eaten == "golden":
                pass
                self.snake_body.append(self.snake_body[-1].copy())
            elif food_eaten:
                pass
            else:
                self.snake_body.pop()
            
            self.update_golden_apple_spawn()
            
            if self.rainbow_effect:
                self.rainbow_timer += 1
                if self.rainbow_timer > 300:
                    self.rainbow_effect = False
                    self.rainbow_timer = 0
            
            self.canvas.delete("all")
            
            if self.grass_photo:
                self.create_grass_background()
            
            self.update_particles()
            
            self.draw_food()
            self.draw_golden_apple()
            self.draw_snake()
            
            self.root.after(self.GAME_SPEED, self.next_turn)
    
    def draw_food(self):
        x, y = self.food_position
        if self.apple_photo:
            self.canvas.create_oval(
                x - 2, y - 2, x + self.UNIT_SIZE + 2, y + self.UNIT_SIZE + 2,
                fill="", outline="#FFD700", width=2
            )
            self.canvas.create_image(
                x + self.UNIT_SIZE // 2,
                y + self.UNIT_SIZE // 2,
                image=self.apple_photo
            )
        else:
            self.canvas.create_oval(
                x - 2, y - 2, x + self.UNIT_SIZE + 2, y + self.UNIT_SIZE + 2,
                fill="", outline="#FFD700", width=2
            )
            self.canvas.create_rectangle(
                x, y, x + self.UNIT_SIZE, y + self.UNIT_SIZE,
                fill="#ff3333", outline="#cc0000", width=2
            )
    
    def draw_golden_apple(self):
        if self.golden_apple_position:
            x, y = self.golden_apple_position
            
            if self.golden_apple_photo:
                self.canvas.create_oval(
                    x - 4, y - 4, x + self.UNIT_SIZE + 4, y + self.UNIT_SIZE + 4,
                    fill="", outline="#FFD700", width=3
                )
                self.canvas.create_oval(
                    x - 2, y - 2, x + self.UNIT_SIZE + 2, y + self.UNIT_SIZE + 2,
                    fill="", outline="#FFA500", width=2
                )
                self.canvas.create_image(
                    x + self.UNIT_SIZE // 2,
                    y + self.UNIT_SIZE // 2,
                    image=self.golden_apple_photo
                )
            else:
                self.canvas.create_oval(
                    x - 4, y - 4, x + self.UNIT_SIZE + 4, y + self.UNIT_SIZE + 4,
                    fill="", outline="#FFD700", width=3
                )
                self.canvas.create_oval(
                    x - 2, y - 2, x + self.UNIT_SIZE + 2, y + self.UNIT_SIZE + 2,
                    fill="", outline="#FFA500", width=2
                )
                self.canvas.create_rectangle(
                    x, y, x + self.UNIT_SIZE, y + self.UNIT_SIZE,
                    fill="#FFD700", outline="#FFA500", width=2
                )
    
    def draw_snake(self):
        for index, (x, y) in enumerate(self.snake_body):
            if index == 0:
                head_color = self.get_rainbow_color() if self.rainbow_effect else self.snake_color
                
                self.canvas.create_rectangle(
                    x + 2, y + 2, x + self.UNIT_SIZE - 2, y + self.UNIT_SIZE - 2,
                    fill=head_color, outline="white", width=2
                )
                
                if self.direction == "right":
                    eye1_x, eye1_y = x + 18, y + 6
                    eye2_x, eye2_y = x + 18, y + 18
                elif self.direction == "left":
                    eye1_x, eye1_y = x + 7, y + 6
                    eye2_x, eye2_y = x + 7, y + 18
                elif self.direction == "up":
                    eye1_x, eye1_y = x + 6, y + 7
                    eye2_x, eye2_y = x + 18, y + 7
                else:
                    eye1_x, eye1_y = x + 6, y + 18
                    eye2_x, eye2_y = x + 18, y + 18
                
                self.canvas.create_oval(eye1_x, eye1_y, eye1_x + 4, eye1_y + 4, fill="black")
                self.canvas.create_oval(eye2_x, eye2_y, eye2_x + 4, eye2_y + 4, fill="black")
            else:
                if self.rainbow_effect:
                    body_color = self.get_rainbow_color(index * 10)
                else:
                    brightness = max(0.3, 1.0 - (index * 0.05))
                    body_color = self.adjust_color_brightness(self.snake_color, brightness)
                
                self.canvas.create_rectangle(
                    x + 1, y + 1, x + self.UNIT_SIZE - 1, y + self.UNIT_SIZE - 1,
                    fill=body_color, outline="#333333", width=1
                )
                
                if index % 2 == 0:
                    scale_color = "#444444" if not self.rainbow_effect else "#666666"
                    self.canvas.create_line(
                        x + 5, y + self.UNIT_SIZE // 2,
                        x + self.UNIT_SIZE - 5, y + self.UNIT_SIZE // 2,
                        fill=scale_color, width=1
                    )
    
    def adjust_color_brightness(self, color, factor):
        color = color.lstrip('#')
        r, g, b = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        r = int(r * factor)
        g = int(g * factor)
        b = int(b * factor)
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def change_direction(self, event):
        new_direction = event.keysym.lower()
        
        if new_direction in ['w', 'up']:
            if self.direction != "down":
                self.direction = "up"
        elif new_direction in ['s', 'down']:
            if self.direction != "up":
                self.direction = "down"
        elif new_direction in ['a', 'left']:
            if self.direction != "right":
                self.direction = "left"
        elif new_direction in ['d', 'right']:
            if self.direction != "left":
                self.direction = "right"
    
    def game_over(self):
        self.game_running = False
        
        is_new_high_score = self.homescreen.update_high_score(self.score)
        
        self.canvas.delete("all")
        
        self.canvas.create_rectangle(
            0, 0, self.BOARD_WIDTH, self.BOARD_HEIGHT,
            fill="black", stipple="gray25"
        )
        
        shadow_offset = 3
        self.canvas.create_text(
            self.BOARD_WIDTH // 2 + shadow_offset,
            self.BOARD_HEIGHT // 2 - 80 + shadow_offset,
            text="GAME OVER",
            font=("Courier", 36, "bold"),
            fill="#333333"
        )
        self.canvas.create_text(
            self.BOARD_WIDTH // 2,
            self.BOARD_HEIGHT // 2 - 80,
            text="GAME OVER",
            font=("Courier", 36, "bold"),
            fill="#FF4444"
        )
        
        if is_new_high_score:
            self.canvas.create_text(
                self.BOARD_WIDTH // 2,
                self.BOARD_HEIGHT // 2 - 40,
                text="NEW HIGH SCORE!",
                font=("Courier", 24, "bold"),
                fill="#FFD700"
            )
        
        stats_text = f"Final Score: {self.score}\nHigh Score: {self.homescreen.high_score}\nLevel Reached: {self.level}\nSnake Length: {len(self.snake_body)}"
        self.canvas.create_rectangle(
            120, 340, 480, 440,
            fill="#222222", outline="#FFD700", width=2
        )
        self.canvas.create_text(
            self.BOARD_WIDTH // 2,
            390,
            text=stats_text,
            font=("Courier", 12),
            fill="white",
            justify="center"
        )
        
        self.canvas.create_text(
            self.BOARD_WIDTH // 2,
            480,
            text="Press R to restart or M for menu",
            font=("Courier", 16),
            fill="#FFD700"
        )
        
        self.root.bind('<KeyPress>', self.restart_or_quit)
    
    def restart_or_quit(self, event):
        key = event.keysym.lower()
        if key == 'r':
            self.restart_game()
        elif key == 'm':
            self.return_to_menu()
    
    def return_to_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.homescreen.high_score = self.homescreen.load_high_score()
        self.homescreen.create_widgets()
    
    def restart_game(self):
        self.snake_body = [[100, 100]]
        self.food_position = self.create_food()
        self.direction = "right"
        self.score = 0
        self.game_running = True
        self.level = 1
        self.snake_color = "#00FF00"
        self.particles = []
        self.GAME_SPEED = 120
        self.golden_apple_position = None
        self.golden_apple_timer = 0
        self.rainbow_effect = False
        self.rainbow_timer = 0
        
        self.update_ui()
        
        self.root.bind('<KeyPress>', self.change_direction)
        
        self.canvas.delete("all")
        if self.grass_photo:
            self.create_grass_background()
        self.draw_food()
        self.draw_golden_apple()
        self.draw_snake()
        
        self.next_turn()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    try:
        from homescreen import MainApp
        app = MainApp()
        app.run()
    except Exception as e:
        print(f"Error: {e}")
        messagebox.showerror("Error", f"Game could not start: {e}")