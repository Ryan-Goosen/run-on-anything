import os
import subprocess

from platform import system
from sys import version_info, executable

def check_if_pip_is_installed():
    try:
        subprocess.run(["pip", "--version"], check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError:
        return False

def install_pip():
    subprocess.run([executable, "-m", "ensurepip"])
    print("\nPIP has been installed.")

def check_uv_is_installed():
    output = subprocess.check_output([executable, '-m', 'pip', 'list'], text=True)
    output = output.split('\n')
    for item in output[2:]:
        if "uv" == item.split(" ")[0].strip():
            print("\nUV is already installed.")
            return True
    return False

def install_uv():
    subprocess.run([executable, '-m', 'pip', 'install', 'uv'])
    print("\nUV has been installed.")

def create_venv(version):
    subprocess.run([executable,"-m","uv", "venv", ".venv", f"--python={version}"], check=True)
    print('\nVirtual Environment Created.')

def install_dependencies():
    req_file = "requirements.txt"
    pp_file = "pyproject.toml"
    lock_file = "uv.lock"
    try:
        if os.path.exists(pp_file):
            print("Found pyproject.toml.")
            if os.path.exists(lock_file):
                print("Found uv.lock. Installing from lockfile...")
                subprocess.run(["uv", "pip", "sync"], check=True)
            else:
                print("No lockfile found. Installing from pyproject.toml...")
                subprocess.run(["uv", "pip", "install"], check=True)

        elif os.path.exists(req_file):
            print("No pyproject.toml found. Falling back to requirements.txt...")
            subprocess.run(["uv", "pip", "install", "-r", req_file], check=True)
        else:
            print("No dependency files found. Continuing without installing packages.")
    except subprocess.CalledProcessError as e:
        print(f"Dependencies installation failed: {e}")

def activate_venv(file_name):
    subprocess.run([python_executable, file_name])

def get_venv_python():
    return os.path.join(".venv", "Scripts", "python.exe") if system() == "Windows" else os.path.join(".venv", "bin", "python")

def setup(file_name, version):
    global python_executable

    if not check_if_pip_is_installed():
        install_pip()
    if not check_uv_is_installed():
        install_uv()
    if not os.path.exists(".venv"):
        create_venv(version)

    python_executable = get_venv_python()
    install_dependencies()
    activate_venv(file_name)


if __name__ == "__main__":
    setup(file_name="main.py", version=3.13)