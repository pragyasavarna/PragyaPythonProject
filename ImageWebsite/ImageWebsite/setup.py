import subprocess
import sys
from pathlib import Path
def install_packages_from_requirements(requirements_file):
    try:
        subprocess.check_call(["pip", "install", "-r", requirements_file])
        print("Packages installed successfully.")
    except subprocess.CalledProcessError as e:
        print("An error occurred while installing packages:", e)


if __name__ == "__main__":
    print("PyCharm is using:", sys.executable)
    BASE_DIR = Path(__file__).resolve().parent.parent
    print(BASE_DIR)
    install_packages_from_requirements("requirements.txt")
