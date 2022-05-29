class identdict(dict):
    def __missing__(self, key):
        return key