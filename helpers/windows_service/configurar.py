import subprocess

from const import FOLDER_ROOT, SERVICE_NAME, NSSM_PATH

command = f"{NSSM_PATH} set {SERVICE_NAME} AppStderr {FOLDER_ROOT}\\var\\logs\\windows_service.log"  # noqa: E501

subprocess.call(command, shell=True)

command = f"{NSSM_PATH} set {SERVICE_NAME} AppDirectory {FOLDER_ROOT}"

subprocess.call(command, shell=True)

command = (
    f"{NSSM_PATH} set {SERVICE_NAME} AppRotateSeconds 86400"  # noqa: E501
)

subprocess.call(command, shell=True)

command = f"{NSSM_PATH} set {SERVICE_NAME} AppStderr {FOLDER_ROOT}\\var\\logs\\windows_service.log"  # noqa: E501

subprocess.call(command, shell=True)

command = f"{NSSM_PATH} set {SERVICE_NAME} Description Serviço para controle de ponto (Visio Telegram Bot)"  # noqa: E501

subprocess.call(command, shell=True)
