import json
import os
import random
from typing import Dict, List

class DataManager:
    def __init__(self, users_file: str = "users.json", words_file: str = "words.json") -> None:
        """
        Initializes the DataManager.
        
        :param users_file: Path to the JSON file storing user progress.
        :param words_file: Path to the JSON file storing game words.
        """
        self.users_file = users_file
        self.words_file = words_file
        self._ensure_files_exist()

    def _ensure_files_exist(self) -> None:
        """Creates default JSON files if they do not exist."""
        if not os.path.exists(self.users_file):
            with open(self.users_file, "w") as f:
                json.dump({}, f)
        if not os.path.exists(self.words_file):
            default_words = {"Easy": ["cat"], "Medium": ["apple"], "Hard": ["python"]}
            with open(self.words_file, "w") as f:
                json.dump(default_words, f)

    def get_users(self) -> Dict[str, int]:
        """
        Retrieves all users and their scores.
        
        :return: A dictionary mapping usernames to their total words spelled.
        """
        with open(self.users_file, "r") as f:
            return json.load(f)

    def save_user_progress(self, username: str, score: int) -> None:
        """
        Updates or creates a user's score.
        
        :param username: The target user's name.
        :param score: The new score to save.
        """
        users = self.get_users()
        users[username] = score
        with open(self.users_file, "w") as f:
            json.dump(users, f, indent=4)

    def get_random_word(self, difficulty: str, previous_word: str = "") -> str:
        """
        Retrieves a random word based on difficulty.
        
        :param difficulty: The requested difficulty level ('Easy', 'Medium', 'Hard').
        :param previous_word: The last word spelled to avoid immediate repetition.
        :return: A random string from the dictionary.
        """
        with open(self.words_file, "r") as f:
            words_dict: Dict[str, List[str]] = json.load(f)
            
        word_list = words_dict.get(difficulty, ["error"])
        if len(word_list) > 1 and previous_word in word_list:
            word_list.remove(previous_word)
            
        return random.choice(word_list)