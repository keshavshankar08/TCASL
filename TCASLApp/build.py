import os
import platform
import shutil
import customtkinter

def build():
    system = platform.system()

    # Clean old build/dist folders first
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists('dist'):
        shutil.rmtree('dist')

    # Common base command
    cmd = 'pyinstaller --noconfirm '

    # Add CustomTkinter library data
    sep = ';' if system == "Windows" else ':'
    ctk_path = customtkinter.__path__[0]

    # Add icons and name
    if system == "Darwin":
        cmd += '--windowed '
        cmd += f'--add-data "{ctk_path}{sep}customtkinter/" '
        cmd += '--name "TCASL" --icon tcasl.icns app.py'
    elif system == "Windows":
        cmd += '--onefile --windowed '
        cmd += f'--add-data "{ctk_path}{sep}customtkinter/" '
        cmd += '--name "TCASL" --icon tcasl.ico app.py'
    else:
        print(f"Unsupported OS: {system}")
        return

    # Run it
    os.system(cmd)

if __name__ == "__main__":
    build()