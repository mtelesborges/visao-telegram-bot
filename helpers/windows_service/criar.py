import os
import sys
import subprocess

from const import FOLDER_ROOT, SERVICE_NAME, NSSM_PATH

python_folder = os.path.dirname(sys.executable)

command = f"{NSSM_PATH} install {SERVICE_NAME} {python_folder}\\python.exe {FOLDER_ROOT}\\main.py"  # noqa: E501

subprocess.call(command, shell=True)
