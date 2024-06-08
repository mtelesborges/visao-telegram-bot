import subprocess

from const import SERVICE_NAME, NSSM_PATH

command = f"{NSSM_PATH} restart {SERVICE_NAME}"

subprocess.call(command, shell=True)
