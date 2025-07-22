import tkinter as tk
from tkinter import messagebox
import random
import os
from PIL import Image, ImageTk
import math

class HomeScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        self.root.geometry("600x700")
        self.root.configure(bg="#0a1f0a")
        self.root.resizable(False, False)
        
        self.animation_frame = 0
        self.snake_demo_positions = []
        
        self.high_score = self.load_high_score()
        
        self.center_window()
        
        self.create_widgets()
        
        self.animate_background()
        
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def create_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()
            
        self.bg_canvas = tk.Canvas(
            self.root,
            width=600,
            height=700,
            bg="#0a1f0a",
            highlightthickness=0
        )
        self.bg_canvas.pack(fill="both", expand=True)
        
        self.create_background_pattern()
        
        title_colors = ["#003300", "#004400", "#005500", "#006600", "#00ff00"]
        for i, color in enumerate(title_colors):
            self.bg_canvas.create_text(
                300 + i, 100 + i,
                text="SNAKE",
                font=("Impact", 64, "bold"),
                fill=color,
                anchor="center"
            )
        
        self.bg_canvas.create_text(
            300, 160,
            text="G A M E",
            font=("Orbitron", 32, "bold"),
            fill="#00cc00",
            anchor="center"
        )
        
        self.bg_canvas.create_rectangle(
            50, 50, 550, 200,
            outline="#00ff00", width=3, fill=""
        )
        
        self.create_demo_snake()
        
        self.bg_canvas.create_text(
            300, 250,
            text="~ CLASSIC ARCADE ACTION ~",
            font=("Courier", 16, "bold"),
            fill="#ffff00",
            anchor="center"
        )
        
        self.create_custom_button()
        
        self.display_high_score()
        
        self.bg_canvas.create_text(
            300, 500,
            text="CONTROLS: WASD or ARROW KEYS",
            font=("Courier", 12, "bold"),
            fill="#888888",
            anchor="center"
        )
        
        self.create_corner_decorations()
            
    def start_game(self):
        try:
            from main import SnakeGame
            game = SnakeGame(self.root, self)
        except Exception as e:
            messagebox.showerror("Error", f"Could not start game: {e}")
    
    def load_high_score(self):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            score_file = os.path.join(current_dir, "highscore.txt")
            
            if os.path.exists(score_file):
                with open(score_file, 'r') as f:
                    return int(f.read().strip())
            else:
                return 0
        except:
            return 0
    
    def save_high_score(self, score):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            score_file = os.path.join(current_dir, "highscore.txt")
            
            with open(score_file, 'w') as f:
                f.write(str(score))
            
            self.high_score = score
        except:
            pass
    
    def update_high_score(self, new_score):
        if new_score > self.high_score:
            self.save_high_score(new_score)
            return True
        return False
    
    def display_high_score(self):
        self.bg_canvas.create_rectangle(
            200, 420, 400, 470,
            fill="#2d4a2d", outline="#FFD700", width=2
        )
        
        self.bg_canvas.create_text(
            300, 435,
            text="HIGH SCORE",
            font=("Courier", 12, "bold"),
            fill="#FFD700",
            anchor="center"
        )
        
        self.bg_canvas.create_text(
            300, 455,
            text=f"{self.high_score:,}",
            font=("Impact", 18, "bold"),
            fill="#FFFFFF",
            anchor="center"
        )
    
    def create_background_pattern(self):
        for x in range(0, 600, 30):
            for y in range(0, 700, 30):
                brightness = random.uniform(0.1, 0.4)
                color = f"#{int(brightness * 255):02x}{int(brightness * 255):02x}{int(brightness * 50):02x}"
                self.bg_canvas.create_oval(
                    x - 1, y - 1, x + 1, y + 1,
                    fill=color, outline="",
                    tags="bg_pattern"
                )
    
    def create_demo_snake(self):
        demo_positions = [
            [480, 300], [460, 300], [440, 300], [420, 300]
        ]
        
        for i, (x, y) in enumerate(demo_positions):
            if i == 0:
                self.bg_canvas.create_rectangle(
                    x, y, x + 15, y + 15,
                    fill="#00ff00", outline="#ffffff", width=1,
                    tags="demo_snake"
                )
            else:
                brightness = 1.0 - (i * 0.2)
                color = f"#{int(brightness * 255):02x}{int(brightness * 255):02x}00"
                self.bg_canvas.create_rectangle(
                    x, y, x + 15, y + 15,
                    fill=color, outline="#333333", width=1,
                    tags="demo_snake"
                )
        
        self.bg_canvas.create_oval(
            520, 295, 535, 310,
            fill="#ff3333", outline="#ffff00", width=2,
            tags="demo_apple"
        )
    
    def create_custom_button(self):
        button_colors = ["#004400", "#005500", "#006600", "#00aa00"]
        for i, color in enumerate(button_colors):
            self.bg_canvas.create_rectangle(
                200 + i, 320 + i, 400 + i, 380 + i,
                fill=color, outline="",
                tags="play_button_bg"
            )
        
        self.bg_canvas.create_rectangle(
            200, 320, 400, 380,
            outline="#00ff00", width=3, fill="",
            tags="play_button"
        )
        
        self.bg_canvas.create_text(
            302, 352,
            text="START GAME",
            font=("Impact", 20, "bold"),
            fill="#003300",
            anchor="center"
        )
        self.bg_canvas.create_text(
            300, 350,
            text="START GAME",
            font=("Impact", 20, "bold"),
            fill="#ffffff",
            anchor="center"
        )
        
        self.bg_canvas.tag_bind("play_button", "<Button-1>", lambda e: self.start_game())
        self.bg_canvas.tag_bind("play_button_bg", "<Button-1>", lambda e: self.start_game())
        
        self.bg_canvas.tag_bind("play_button", "<Enter>", self.button_hover_enter)
        self.bg_canvas.tag_bind("play_button", "<Leave>", self.button_hover_leave)
        self.bg_canvas.tag_bind("play_button_bg", "<Enter>", self.button_hover_enter)
        self.bg_canvas.tag_bind("play_button_bg", "<Leave>", self.button_hover_leave)
    
    def button_hover_enter(self, event):
        self.bg_canvas.itemconfig("play_button", outline="#ffff00", width=4)
    
    def button_hover_leave(self, event):
        self.bg_canvas.itemconfig("play_button", outline="#00ff00", width=3)
    
    def create_corner_decorations(self):
        for i in range(5):
            self.bg_canvas.create_line(
                10 + i * 5, 10, 10, 10 + i * 5,
                fill="#00aa00", width=2
            )
        
        for i in range(5):
            self.bg_canvas.create_line(
                590 - i * 5, 10, 590, 10 + i * 5,
                fill="#00aa00", width=2
            )
        
        for i in range(5):
            self.bg_canvas.create_line(
                10 + i * 5, 690, 10, 690 - i * 5,
                fill="#00aa00", width=2
            )
        
        for i in range(5):
            self.bg_canvas.create_line(
                590 - i * 5, 690, 590, 690 - i * 5,
                fill="#00aa00", width=2
            )
    
    def animate_background(self):
        self.animation_frame += 1
        
        if self.animation_frame % 30 == 0:
            self.bg_canvas.delete("demo_snake")
            self.bg_canvas.delete("demo_apple")
            
            base_x = 400 + int(50 * math.sin(self.animation_frame * 0.1))
            demo_positions = [
                [base_x + 80, 300], [base_x + 60, 300], 
                [base_x + 40, 300], [base_x + 20, 300]
            ]
            
            for i, (x, y) in enumerate(demo_positions):
                if i == 0:
                    self.bg_canvas.create_rectangle(
                        x, y, x + 15, y + 15,
                        fill="#00ff00", outline="#ffffff", width=1,
                        tags="demo_snake"
                    )
                else:
                    brightness = 1.0 - (i * 0.2)
                    color = f"#{int(brightness * 255):02x}{int(brightness * 255):02x}00"
                    self.bg_canvas.create_rectangle(
                        x, y, x + 15, y + 15,
                        fill=color, outline="#333333", width=1,
                        tags="demo_snake"
                    )
            
            apple_x = base_x + 120
            self.bg_canvas.create_oval(
                apple_x, 295, apple_x + 15, 310,
                fill="#ff3333", outline="#ffff00", width=2,
                tags="demo_apple"
            )
        
        self.root.after(50, self.animate_background)

class MainApp:
    def __init__(self):
        self.root = tk.Tk()
        self.homescreen = HomeScreen(self.root)
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MainApp()
    app.run()