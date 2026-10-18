import logging

logger = logging.getLogger("banka")
logger.setLevel(logging.DEBUG)


console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_formatter = logging.Formatter("%(levelname)-8s: %(message)s")
console_handler.setFormatter(console_formatter)


file_handler = logging.FileHandler("banka.log", mode="w", encoding="utf-8")
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter("%(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)


logger.addHandler(console_handler)
logger.addHandler(file_handler)


class BankovniUcet:
    def __init__(self, majitel: str, zustatek: float = 0):
        self.majitel = majitel
        self.zustatek = zustatek
        logger.info(f"Účet vytvořen: {self.majitel}, zůstatek = {self.zustatek} Kč.")

    def vlozit(self, castka):
        self.zustatek += castka
        logger.info(f"{self.majitel}: vklad {castka} Kč. Nový zůstatek = {self.zustatek} Kč.")

    def vybrat(self, castka):
        if self.zustatek < castka:
            logger.warning(f"{self.majitel}: nedostatek prostředků pro výběr {castka} Kč (zůstatek = {self.zustatek} Kč).")
        else:
            self.zustatek -= castka

    def prevod(self, cilovy_ucet, castka):
        if self.zustatek < castka:
            logger.error(f"{self.majitel}: nedostatek prostředků pro převod {castka} (zůstatek = {self.zustatek} Kč) na cílový účet {cilovy_ucet}.")
        else:
            zustatek_pred = self.zustatek
            cilovy_zust_pred = cilovy_ucet.zustatek
            self.zustatek -= castka
            cilovy_ucet.zustatek += castka
            logger.info(f"Převod {castka} Kč z {self.majitel} na {cilovy_ucet.majitel}.")

            logger.debug(f"{self.majitel}: zůstatek {zustatek_pred} Kč -> {self.zustatek} Kč.")
            logger.debug(f"{cilovy_ucet.majitel}: zůstatek {cilovy_zust_pred} Kč -> {cilovy_ucet.zustatek} Kč.")


alice = BankovniUcet("Alice", 1000.0)
bob = BankovniUcet("Bob", 500.0)

alice.vlozit(500)
bob.vybrat(1000)

alice.prevod(bob, 200)

print(f"==============\nKonečné zůstatky: Alice = {alice.zustatek} Kč, Bob = {bob.zustatek} Kč.")

print("\n--- Obsah souboru ---")
with open("banka.log", "r") as file:
    content = file.read()
    print(content)