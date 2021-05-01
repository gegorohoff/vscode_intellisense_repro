from labtech.utils.api.api import APIHelper


class Helper:
    def main(self):
        _api = APIHelper()
        print(_api.login_api('joe','supersecure'))

if __name__ == "__main__":
    main()
