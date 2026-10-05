import logging

# Kořenový logger
root_logger = logging.getLogger()

# Pojmenované loggery v hierarchii
app_logger = logging.getLogger("cviceni1")

# Přidáme handler na root logger (všechny zprávy se sem dostanou)
console = logging.StreamHandler()
console.setFormatter(logging.Formatter("%(name)s - %(levelname)s - %(message)s"))
root_logger.addHandler(console)
root_logger.setLevel(logging.DEBUG)

# Zprávy z různých loggerů
root_logger.info("Zpráva z root loggeru")
app_logger.info("Zpráva z app loggeru")