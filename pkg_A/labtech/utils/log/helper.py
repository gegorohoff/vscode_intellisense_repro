from labtech.utils.log.log import Logger


class Helper:

    def main(self):
        _log = Logger()
        print(_log.get_logs())

if __name__ == "__main__":
    Helper().main()
