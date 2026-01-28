import logging
import requests
from colorlog import ColoredFormatter


# CONFIGURACIÓN GLOBAL
logging.raiseExceptions = True  


# CONFIGURACIÓN TELEGRAM

TELEGRAM_TOKEN = "7707290031:AAH81v7dFMngypSt6IY42gS6uuv1HgzkF4g"
TELEGRAM_CHAT_ID = "1164415265"


class TelegramHandler(logging.Handler):
    def __init__(self):
        super().__init__()

    def emit(self, record):
        log_entry = self.format(record)
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": log_entry
        }
        try:
            r = requests.post(url, json=payload, timeout=5)
            r.raise_for_status()
        except Exception as e:
            print("Error enviando log a Telegram:", e)


# CONFIGURACIÓN LOGGER

logger = logging.getLogger("LoggerAvanzado")
logger.setLevel(logging.DEBUG)
logger.propagate = False

# Evitar duplicar handlers si se ejecuta más de una vez
if logger.handlers:
    logger.handlers.clear()


# FORMATO GENERAL

formato = (
    "%(log_color)s[%(levelname)s] "
    "%(asctime)s - "
    "%(filename)s - "
    "%(message)s"
)


# HANDLER CONSOLA (COLOR)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_formatter = ColoredFormatter(
    formato,
    datefmt="%Y-%m-%d %H:%M:%S",
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red'
    }
)
console_handler.setFormatter(console_formatter)


# HANDLER ARCHIVO

file_handler = logging.FileHandler("aplicacion.log", mode="a", encoding="utf-8")
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter(
    "[%(levelname)s] %(asctime)s - %(filename)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
file_handler.setFormatter(file_formatter)


# HANDLER TELEGRAM

telegram_handler = TelegramHandler()
telegram_handler.setLevel(logging.ERROR)
telegram_formatter = logging.Formatter(
    " %(levelname)s\n %(asctime)s\n %(filename)s\n %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
telegram_handler.setFormatter(telegram_formatter)


# AGREGAR HANDLERS
logger.addHandler(console_handler)
logger.addHandler(file_handler)
logger.addHandler(telegram_handler)


# EJEMPLOS DE LOGGING

logger.debug("Mensaje de depuración")
logger.info("Inicio correcto del programa")
logger.warning("Advertencia detectada")
logger.error("Error en la ejecución")
logger.critical("Fallo crítico del sistema")
