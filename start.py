import subprocess
import time
from colorama import init, Fore

init(autoreset=True)

def run_script(script_path, params):
    # Run the script file with parameters
    subprocess.call(['python', script_path, str(params)])

def display_features():
    # Function to display available features
    print(Fore.LIGHTGREEN_EX + "Fitur Tersedia:")
    print(Fore.LIGHTGREEN_EX + "1. View Bot v2")
    print(Fore.LIGHTGREEN_EX + "2. View Bot v1")
    print(Fore.LIGHTGREEN_EX + "3. Gmail Login Bot")

# Auto Views Youtube 0.1.0
print(Fore.LIGHTGREEN_EX + "+-------------------------- Version: 0.1.0 --------------------------+")

display_features()
# Prompt the user for input
feature_input = input(Fore.LIGHTYELLOW_EX + "Silahkan Pilih Fitur Yang Tersedia: ")

print(Fore.LIGHTYELLOW_EX + "Fitur Dipilih:", feature_input)

# Get max_watch from user
max_watch = input(Fore.LIGHTYELLOW_EX + "Masukan Lama Waktu Menonton (default: 5): ")
if not max_watch:
    max_watch = 5
else:
    max_watch = int(max_watch)

print(Fore.LIGHTYELLOW_EX + "Menonton:", (max_watch),"Menit")   

# Run the script based on user input
if feature_input == "1":
    run_script('viewer2.py', max_watch)
elif feature_input == "2":
    run_script('viewer1.py', max_watch)
elif feature_input == "3":
    run_script('gmail.py', max_watch)
else:
    print("Invalid choice. Please try again.") 



