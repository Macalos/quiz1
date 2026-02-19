import tkinter as tk
from tkinter import font as tkfont
import random
import time


C_BG     = "#050506" 
C_FRAME  = "#121214" 
C_CYAN   = "#00F3FF" 
C_PINK   = "#FF00FF" 
C_GREEN  = "#39FF14" 
C_YELLOW = "#F9DB00" 
C_RED    = "#FF3131" 

class SimpleCyberBattle:
    def __init__(self, window):
        self.window = window 
        self.window.title("TIC_TAC_TOE")
        self.window.geometry("1000x850")
        self.window.config(bg=C_BG)
       
        self.current_player = "X"
        self.is_game_over = False
        self.score_x = 0
        self.score_o = 0
        self.score_draws = 0
        
        self.faces = {
            "IDLE": ["( •_• )", "( ._. )"],
            "MOVE": ["( o_o )", "( @ @ )"],
            "WIN":  ["( ^▽^ )/", "( ≧◡≦ )"],
            "LOSE": ["( T_T )", "( >_< )"],
            "DRAW": ["( ºΔº )", "( -_- )"]
        }

        self.setup_fonts()
        self.build_ui()

    def setup_fonts(self):
        
        self.font_small  = tkfont.Font(family="Consolas", size=11, weight="bold")
        self.font_medium = tkfont.Font(family="Consolas", size=20, weight="bold")
        self.font_large  = tkfont.Font(family="Consolas", size=40, weight="bold")
        self.font_pet    = tkfont.Font(family="Courier",  size=36, weight="bold")

    def build_ui(self):
      
        self.header = tk.Frame(self.window, bg=C_BG, pady=20)
        self.header.pack(fill="x")

        
        self.box_x = tk.Frame(self.header, bg=C_FRAME, highlightbackground=C_CYAN, highlightthickness=2, padx=20, pady=10)
        self.box_x.pack(side="left", padx=50)
        tk.Label(self.box_x, text="X WINS", font=self.font_small, bg=C_FRAME, fg=C_CYAN).pack()
        self.lbl_score_x = tk.Label(self.box_x, text="00", font=self.font_medium, bg=C_FRAME, fg="white")
        self.lbl_score_x.pack()

       
        self.box_draw = tk.Frame(self.header, bg=C_FRAME, highlightbackground=C_YELLOW, highlightthickness=1, padx=15, pady=5)
        self.box_draw.pack(side="left", expand=True)
        tk.Label(self.box_draw, text="DRAW", font=self.font_small, bg=C_FRAME, fg=C_YELLOW).pack()
        self.lbl_score_draw = tk.Label(self.box_draw, text="00", font=self.font_small, bg=C_FRAME, fg="white")
        self.lbl_score_draw.pack()

       
        self.box_o = tk.Frame(self.header, bg=C_FRAME, highlightbackground=C_PINK, highlightthickness=2, padx=20, pady=10)
        self.box_o.pack(side="right", padx=50)
        tk.Label(self.box_o, text="O WINS", font=self.font_small, bg=C_FRAME, fg=C_PINK).pack()
        self.lbl_score_o = tk.Label(self.box_o, text="00", font=self.font_medium, bg=C_FRAME, fg="white")
        self.lbl_score_o.pack()

        
        self.announcer = tk.Label(self.window, text=">>> X TURN <<<", font=self.font_medium, bg=C_BG, fg=C_CYAN, pady=20)
        self.announcer.pack()

       
        self.arena = tk.Frame(self.window, bg=C_BG)
        self.arena.pack(expand=True, fill="both")

         
        self.pet_x = tk.Label(self.arena, text=self.faces["IDLE"][0], font=self.font_pet, bg=C_BG, fg=C_CYAN)
        self.pet_x.place(relx=0.15, rely=0.35, anchor="center")
        tk.Button(self.arena, text="NEXT ROUND", bg=C_FRAME, fg=C_CYAN, relief="flat", command=self.next_round_reset).place(relx=0.15, rely=0.55, anchor="center")

        
        self.grid_container = tk.Frame(self.arena, bg=C_CYAN, padx=2, pady=2)
        self.grid_container.place(relx=0.5, rely=0.4, anchor="center")
        self.board_inner = tk.Frame(self.grid_container, bg=C_BG)
        self.board_inner.pack()

        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for row in range(3):
            for col in range(3):
                btn = tk.Button(self.board_inner, text="", font=self.font_large, width=4, height=1,
                                bg=C_FRAME, fg="white", relief="flat", bd=0,
                                command=lambda r=row, c=col: self.handle_click(r, c))
                btn.grid(row=row, column=col, padx=3, pady=3)
                self.buttons[row][col] = btn

       
        self.pet_o = tk.Label(self.arena, text=self.faces["IDLE"][0], font=self.font_pet, bg=C_BG, fg=C_PINK)
        self.pet_o.place(relx=0.85, rely=0.35, anchor="center")
        tk.Button(self.arena, text="RESET SCORES", bg=C_FRAME, fg=C_RED, relief="flat", command=self.full_game_reset).place(relx=0.85, rely=0.55, anchor="center")

    
    def handle_click(self, r, c):
        
        button_clicked = self.buttons[r][c]
        
       
        if button_clicked["text"] == "" and not self.is_game_over:
           
            color = C_CYAN if self.current_player == "X" else C_PINK
            button_clicked.config(text=self.current_player, fg=color)
            
            
            self.pet_x.config(text=random.choice(self.faces["MOVE"]))
            self.pet_o.config(text=random.choice(self.faces["MOVE"]))

            
            if self.check_for_winner():
                self.handle_win()
            elif self.check_for_draw():
                self.handle_draw()
            else:
                
                if self.current_player == "X":
                    self.current_player = "O"
                else:
                    self.current_player = "X"
                
                
                new_color = C_CYAN if self.current_player == "X" else C_PINK
                self.announcer.config(text=f">>> {self.current_player} TURN <<<", fg=new_color)

    def check_for_winner(self):
        """ Scans the board for 3 in a row """
        b = self.buttons
       
        lines = [
            [(0,0),(0,1),(0,2)], [(1,0),(1,1),(1,2)], [(2,0),(2,1),(2,2)],
            [(0,0),(1,0),(2,0)], [(0,1),(1,1),(2,1)], [(0,2),(1,2),(2,2)], 
            [(0,0),(1,1),(2,2)], [(0,2),(1,1),(2,0)]                      
        ]
        for line in lines:
            p1, p2, p3 = line
            if b[p1[0]][p1[1]]["text"] == b[p2[0]][p2[1]]["text"] == b[p3[0]][p3[1]]["text"] != "":
                self.winning_line = line
                return True
        return False

    def check_for_draw(self):
       
        for row in range(3):
            for col in range(3):
                if self.buttons[row][col]["text"] == "":
                    return False
        return True

    def handle_win(self):
        self.is_game_over = True
        winner = self.current_player
        win_color = C_CYAN if winner == "X" else C_PINK
        
        self.announcer.config(text=f"WINNER: PLAYER {winner}", fg=win_color)
        
       
        if winner == "X": self.score_x += 1
        else: self.score_o += 1
        self.update_score_labels()

        
        if winner == "X":
            self.pet_x.config(text=random.choice(self.faces["WIN"]), fg=C_GREEN)
            self.pet_o.config(text=random.choice(self.faces["LOSE"]), fg=C_RED)
        else:
            self.pet_o.config(text=random.choice(self.faces["WIN"]), fg=C_GREEN)
            self.pet_x.config(text=random.choice(self.faces["LOSE"]), fg=C_RED)

       
        for _ in range(4):
            for r, c in self.winning_line: self.buttons[r][c].config(bg=win_color, fg=C_BG)
            self.window.update(); time.sleep(0.08)
            for r, c in self.winning_line: self.buttons[r][c].config(bg="white", fg=C_BG)
            self.window.update(); time.sleep(0.08)
        for r, c in self.winning_line: self.buttons[r][c].config(bg=win_color, fg=C_BG)

    def handle_draw(self):
        self.is_game_over = True
        self.score_draws += 1
        self.update_score_labels()
        self.announcer.config(text="DRAW ", fg=C_YELLOW)
        self.pet_x.config(text=random.choice(self.faces["DRAW"]), fg=C_YELLOW)
        self.pet_o.config(text=random.choice(self.faces["DRAW"]), fg=C_YELLOW)
        for r in range(3):
            for c in range(3): self.buttons[r][c].config(bg=C_YELLOW, fg=C_BG)

    def update_score_labels(self):
        self.lbl_score_x.config(text=f"{self.score_x:02d}")
        self.lbl_score_o.config(text=f"{self.score_o:02d}")
        self.lbl_score_draw.config(text=f"{self.score_draws:02d}")

    def next_round_reset(self):
        
        self.is_game_over = False
        self.current_player = "X"
        self.announcer.config(text=">>> X TURN <<<", fg=C_CYAN)
        self.pet_x.config(text=self.faces["IDLE"][0], fg=C_CYAN)
        self.pet_o.config(text=self.faces["IDLE"][0], fg=C_PINK)
        for r in range(3):
            for col in range(3):
                self.buttons[r][col].config(text="", bg=C_FRAME, fg="white")

    def full_game_reset(self):
        
        self.score_x = 0
        self.score_o = 0
        self.score_draws = 0
        self.update_score_labels()
        self.next_round_reset()

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleCyberBattle(root)
    root.mainloop()