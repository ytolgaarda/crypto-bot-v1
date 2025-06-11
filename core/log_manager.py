class LogManager:
    def __init__(self, filename="trade_log.txt"):
        self.filename = filename

    def write(self, message: str):
        with open(self.filename, "a") as log_file:
            log_file.write(message + "\n")
