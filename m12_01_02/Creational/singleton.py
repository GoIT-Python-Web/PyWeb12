class Singleton:
    """Classic singleton"""

    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(Singleton)
        return cls.__instance


if __name__ == '__main__':
    s1 = Singleton()
    s2 = Singleton()

    print(s1 == s2)
    print(s1 is s2)
