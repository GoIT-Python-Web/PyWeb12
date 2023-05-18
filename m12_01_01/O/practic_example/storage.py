import json
import yaml


class Storage:
    def get_value(self, key):
        raise NotImplementedError


class JSONStorage(Storage):
    def __init__(self, filename):
        self.filename = filename

    def get_value(self, key):
        with open(self.filename, 'r') as fd:
            data = json.load(fd)
            return data.get(key)


class YamlStorage(Storage):
    def __init__(self, filename):
        self.filename = filename

    def get_value(self, key):
        with open(self.filename, 'r') as fd:
            data = yaml.load(fd, Loader=yaml.FullLoader)
            return data.get(key)


class Service:
    def __init__(self, storage: Storage):
        self.storage = storage

    def get(self, key):
        return self.storage.get_value(key)


if __name__ == '__main__':
    sj = Service(JSONStorage('data.json'))
    print(sj.get('name'), sj.get('age'))

    sj = Service(YamlStorage('data.yaml'))
    print(sj.get('name'), sj.get('age'))
