import json
import os
import sys
import random
import platform
from typing import Dict, List


def get_user_data_dir() -> str:
    """
    Returns a writable, OS-appropriate directory for storing user data.
    This is necessary because .app bundles and .exe files are read-only
    after packaging — user progress must be stored outside the bundle.

    - macOS:   ~/Library/Application Support/TCASL/
    - Windows: %APPDATA%/TCASL/
    - Linux:   ~/.tcasl/
    """
    system = platform.system()
    if system == "Darwin":
        base = os.path.expanduser("~/Library/Application Support")
    elif system == "Windows":
        base = os.environ.get("APPDATA", os.path.expanduser("~"))
    else:
        base = os.path.expanduser("~")
    path = os.path.join(base, "TCASL")
    os.makedirs(path, exist_ok=True)
    return path


def get_bundled_resource_path(relative_path: str) -> str:
    """
    Returns the correct path to a read-only resource file (e.g. words.json).
    Works both when running from source and when frozen by PyInstaller.
    """
    try:
        # PyInstaller extracts files to sys._MEIPASS at runtime
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class DataManager:
    def __init__(self, words_file: str = "words.json") -> None:
        """
        Initializes the DataManager.

        users.json is stored in the OS user-data directory (writable).
        words.json is bundled as a read-only resource inside the app.

        :param words_file: Filename of the bundled words resource.
        """
        self.users_file = os.path.join(get_user_data_dir(), "users.json")
        self.words_file = get_bundled_resource_path(words_file)
        self._ensure_users_file_exists()

    def _ensure_users_file_exists(self) -> None:
        """Creates a default users.json in the user-data dir if missing."""
        if not os.path.exists(self.users_file):
            with open(self.users_file, "w") as f:
                json.dump({}, f)

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