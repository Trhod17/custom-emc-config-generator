import logging

from rich.logging import RichHandler

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
FORMAT = "%(message)s"
logging.basicConfig(
    level=logging.NOTSET, format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger("")


fileHandler = logging.FileHandler(filename="debug.log", mode="w")
fileHandler.setFormatter(formatter)
log.addHandler(fileHandler)

# consoleHandler = logging.StreamHandler()
# log.addHandler(consoleHandler)


log.info("Starting Log!")
