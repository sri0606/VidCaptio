import os
import sys
import subprocess
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--create_exe", action="store_true",
                        help="Create an executable using Nuitka")
    args = parser.parse_args()

    # Step 0: Upgrade pip
    print("Upgrading pip...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])

    # Step 1: Install dependencies
    print("Installing dependencies...")
    subprocess.check_call(["pip", "install", "-r", "requirements.txt"])

    if args.create_exe:
        # Step 2: Install Nuitka and create an executable
        print("Installing Nuitka to create a simple exe (not standalone)...")
        subprocess.check_call(["pip", "install", "Nuitka"])
        print("Creating executable...")
        subprocess.check_call(["python", "-m", "nuitka", "run.py"])

    # Step 3: Create a projects directory
    if not os.path.exists('projects/'):
        os.makedirs('projects/')

    print(f"Setup is done. Any future projects you will create will be stored in this directory: {os.path.abspath('projects/')}.")

