import sys
import os
import customtkinter as ctk
import cv2 as cv
from PIL import Image
import time
from data_manager import DataManager
from backend import GameEngine

def resource_path(relative_path):
    """Get the absolute path to a resource in a bundled app."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class TCASLApp(ctk.CTk):
    """The main graphical user interface for the TCASL game."""
    
    def __init__(self) -> None:
        """Initializes the application window and core components."""
        super().__init__()
        self.title("TCASL Learner")
        self.geometry("900x700")
        
        self.data_mgr = DataManager()
        self.engine = GameEngine()
        
        self.current_user: str = ""
        self.words_spelled: int = 0
        self.stream_running: bool = False
        self.current_word: str = ""
        self.current_letter_idx: int = 0
        self.cooldown_time: float = 0.0
        self.letter_labels: list = []
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.show_login_screen()

    def show_login_screen(self) -> None:
        """Renders the login UI."""
        self._clear_window()
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(frame, text="Welcome to TCASL Learner", font=("Helvetica", 28, "bold")).pack(pady=20)
        
        users = self.data_mgr.get_users()
        user_list = list(users.keys()) if users else ["No users found"]
        
        self.user_var = ctk.StringVar(value=user_list[0])
        self.user_dropdown = ctk.CTkOptionMenu(frame, variable=self.user_var, values=user_list, width=200)
        self.user_dropdown.pack(pady=10)
        
        ctk.CTkButton(frame, text="Load Profile", command=self.load_profile, width=200).pack(pady=10)
        
        ctk.CTkLabel(frame, text="Or create a new profile:", font=("Helvetica", 14)).pack(pady=(20, 5))
        self.new_user_entry = ctk.CTkEntry(frame, placeholder_text="Enter name...", width=200)
        self.new_user_entry.pack(pady=5)
        
        ctk.CTkButton(frame, text="Create Profile", command=self.create_profile, width=200, fg_color="green", hover_color="darkgreen").pack(pady=10)

    def load_profile(self) -> None:
        """Loads data for the selected existing user."""
        user = self.user_var.get()
        if user and user != "No users found":
            self.current_user = user
            self.words_spelled = self.data_mgr.get_users().get(user, 0)
            self.show_setup_screen()

    def create_profile(self) -> None:
        """Registers a new user and saves their initial profile."""
        new_name = self.new_user_entry.get().strip()
        if new_name:
            self.current_user = new_name
            self.words_spelled = 0
            self.data_mgr.save_user_progress(new_name, 0)
            self.show_setup_screen()

    def show_setup_screen(self) -> None:
        """Renders the game configuration UI."""
        self._clear_window()
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(frame, text=f"Profile: {self.current_user}", font=("Helvetica", 24, "bold")).pack(pady=5)
        ctk.CTkLabel(frame, text=f"Total Words Spelled: {self.words_spelled}", font=("Helvetica", 16), text_color="gray").pack(pady=(0, 30))
        
        ctk.CTkLabel(frame, text="Select Camera:", font=("Helvetica", 14)).pack()
        self.cam_var = ctk.StringVar(value="0")
        ctk.CTkOptionMenu(frame, variable=self.cam_var, values=["0", "1", "2", "3"], width=200).pack(pady=10)
        
        ctk.CTkLabel(frame, text="Select Difficulty:", font=("Helvetica", 14)).pack(pady=(20,0))
        self.diff_var = ctk.StringVar(value="Easy")
        ctk.CTkOptionMenu(frame, variable=self.diff_var, values=["Easy", "Medium", "Hard"], width=200).pack(pady=10)
        
        ctk.CTkButton(frame, text="Start Game", command=self.start_game, width=200, height=40, font=("Helvetica", 16, "bold")).pack(pady=30)
        ctk.CTkButton(frame, text="Switch User", command=self.show_login_screen, fg_color="transparent", border_width=1, text_color="gray").pack()

    def start_game(self) -> None:
        """Initializes the backend components and transitions to the game loop."""
        cam_idx = int(self.cam_var.get())
        if not self.engine.start_camera(cam_idx):
            print("Failed to open camera!")
            return
            
        self.stream_running = True
        self._clear_window()
        self._build_game_ui()
        self.load_new_word()
        self.process_video_loop()

    def _build_game_ui(self) -> None:
        """Constructs the layout for the active gameplay screen."""
        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.pack(fill="x", pady=20, padx=20)
        
        self.lbl_stats = ctk.CTkLabel(top_frame, text=f"Words Spelled: {self.words_spelled}", font=("Helvetica", 16, "bold"), text_color="black")
        self.lbl_stats.pack(side="left")
        
        self.wordle_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        self.wordle_frame.pack(side="top", expand=True)
        
        vid_frame = ctk.CTkFrame(self, fg_color="transparent")
        vid_frame.pack(expand=True)
        
        self.lbl_orig = ctk.CTkLabel(vid_frame, text="")
        self.lbl_orig.pack(side="left", padx=10)
        self.lbl_tc = ctk.CTkLabel(vid_frame, text="")
        self.lbl_tc.pack(side="left", padx=10)
        
        self.conf_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.conf_frame.pack(pady=10)
        
        self.lbl_conf = ctk.CTkLabel(self.conf_frame, text="Gesture Quality: 0%", font=("Helvetica", 14))
        self.lbl_conf.pack()
        
        self.conf_bar = ctk.CTkProgressBar(self.conf_frame, width=300, progress_color="green")
        self.conf_bar.set(0.0)
        self.conf_bar.pack(pady=5)
        
        bot_frame = ctk.CTkFrame(self, fg_color="transparent")
        bot_frame.pack(side="bottom", pady=20)
        
        ctk.CTkButton(bot_frame, text="Skip Word", command=self.load_new_word, fg_color="orange", hover_color="darkorange").pack(side="left", padx=10)
        ctk.CTkButton(bot_frame, text="End Game", command=self.end_game, fg_color="red", hover_color="darkred").pack(side="left", padx=10)

    def load_new_word(self) -> None:
        """Fetches a new word from the DataManager and resets gameplay state."""
        diff = self.diff_var.get()
        self.current_word = self.data_mgr.get_random_word(diff, previous_word=self.current_word)
        self.current_letter_idx = 0
        self.engine.clear_buffer()
        self.render_wordle_boxes()

    def render_wordle_boxes(self) -> None:
        """Updates the visual representation of the current word being spelled."""
        for widget in self.wordle_frame.winfo_children():
            widget.destroy()
        self.letter_labels.clear()
        
        for i, char in enumerate(self.current_word):
            if i < self.current_letter_idx:
                bg, border, txt_color = "green", 0, "white"
            elif i == self.current_letter_idx:
                bg, border, txt_color = "transparent", 2, "black"
            else:
                bg, border, txt_color = "gray70", 0, "white"
                
            lbl = ctk.CTkLabel(self.wordle_frame, text=char.upper(), font=("Helvetica", 32, "bold"), width=60, height=60, corner_radius=10, fg_color=bg, text_color=txt_color)
            
            if i == self.current_letter_idx:
                border_frame = ctk.CTkFrame(self.wordle_frame, border_width=3, border_color="#000000", corner_radius=10, fg_color="transparent")
                border_frame.pack(side="left", padx=5)
                inner_lbl = ctk.CTkLabel(border_frame, text=char.upper(), font=("Helvetica", 32, "bold"), width=54, height=54)
                inner_lbl.pack(padx=3, pady=3)
                self.letter_labels.append(inner_lbl)
            else:
                lbl.pack(side="left", padx=5)
                self.letter_labels.append(lbl)

    def handle_correct_letter(self) -> None:
        """Processes logic when a user correctly signs the targeted letter."""
        self.current_letter_idx += 1
        self.engine.clear_buffer()
        self.cooldown_time = time.time() + 2.0
        
        if self.current_letter_idx >= len(self.current_word):
            self.words_spelled += 1
            self.lbl_stats.configure(text=f"Words Spelled: {self.words_spelled}")
            self.data_mgr.save_user_progress(self.current_user, self.words_spelled)
            self.after(1000, self.load_new_word)
        
        self.render_wordle_boxes()

    def process_video_loop(self) -> None:
        """Recursively polls the engine for frames and updates the UI."""
        if not self.stream_running:
            return

        orig_frame, tc_frame, pred = self.engine.process_frame()

        if orig_frame is not None and tc_frame is not None:
            if self.current_letter_idx < len(self.current_word):
                target_char = self.current_word[self.current_letter_idx].lower()
                
                avg_conf = self.engine.get_target_confidence(target_char)
                self.conf_bar.set(avg_conf / 100.0)
                self.lbl_conf.configure(text=f"Gesture Quality: {int(avg_conf)}%")

                if time.time() > self.cooldown_time:
                    if pred == target_char:
                        self.handle_correct_letter()

            display_orig = cv.cvtColor(orig_frame, cv.COLOR_GRAY2RGB)
            img_orig = ctk.CTkImage(light_image=Image.fromarray(display_orig), size=(256, 256))
            img_tc = ctk.CTkImage(light_image=Image.fromarray(tc_frame), size=(256, 256))

            self.lbl_orig.configure(image=img_orig)
            self.lbl_tc.configure(image=img_tc)

        self.after(30, self.process_video_loop)

    def end_game(self) -> None:
        """Terminates the active game session and returns to setup."""
        self.stream_running = False
        self.engine.stop_camera()
        self.show_setup_screen()

    def _clear_window(self) -> None:
        """Removes all active child widgets from the root window."""
        for widget in self.winfo_children():
            widget.destroy()

    def on_closing(self) -> None:
        """Handles teardown routines during application exit."""
        self.stream_running = False
        self.engine.stop_camera()
        self.destroy()

if __name__ == "__main__":
    app = TCASLApp()
    app.mainloop()