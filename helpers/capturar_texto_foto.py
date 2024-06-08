from PIL import Image
from pytesseract import pytesseract
from configs.logger import logger


def capturar_texto_foto(path_to_image):
    try:
        # Define path to tessaract.exe
        path_to_tesseract = "C:\\Users\\teles\\Projetos\\visio-telegram-bot\\libs\\tesseract\\tesseract.exe"  # noqa: E501
        # Define path to image
        # Point tessaract_cmd to tessaract.exe
        pytesseract.tesseract_cmd = path_to_tesseract
        # Open image with PIL
        img = Image.open(path_to_image)
        # Extract text from image
        text = pytesseract.image_to_string(img)
        return text
    except Exception as error:
        logger.error(
            f"Falha ao capturar o texto da imagem {path_to_image}.\nErro: {error}"  # noqa: E501
        )
