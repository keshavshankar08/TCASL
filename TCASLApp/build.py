import os
import platform
import shutil
import customtkinter


def build():
    system = platform.system()

    for folder in ("build", "dist"):
        if os.path.exists(folder):
            shutil.rmtree(folder)

    ctk_path = customtkinter.__path__[0]
    sep = ";" if system == "Windows" else ":"

    flags = [
        "pyinstaller",
        "--noconfirm",
        "--windowed",
        "--name TCASL",

        f'--add-data "words.json{sep}."',

        f'--add-data "{ctk_path}{sep}customtkinter/"',

        "--collect-all torch",
        "--collect-all torchvision",

        "--collect-all lava",
        "--collect-all lava_dl",

        "--collect-all tcasl",

        "--hidden-import cv2",
        "--hidden-import PIL._tkinter_finder",
        "--hidden-import numpy",
        "--hidden-import customtkinter",

        "--hidden-import torch.distributions",
        "--hidden-import torch.distributions.constraints",
        "--hidden-import torch.distributions.utils",

        "--noconfirm",
    ]

    if system == "Darwin":
        flags += [
            "--icon tcasl.icns",
            "app.py",
        ]
    elif system == "Windows":
        flags += [
            "--onefile",
            "--icon tcasl.ico",
            "app.py",
        ]
    else:
        print(f"Unsupported OS: {system}")
        return

    cmd = " ".join(flags)
    print(f"\nRunning:\n{cmd}\n")
    os.system(cmd)


if __name__ == "__main__":
    build()