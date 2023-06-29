import redis
import pickle

client = redis.Redis(host='localhost', port=6379, password=None)

if __name__ == '__main__':
    client.set('user1', "Yops Today")
    client.set('user2', "Evgen Tr")
    client.expire('user2', 600)
    client.set('num', 123)
    client.set('lnum', pickle.dumps([42, 13, 7]))
    client.delete('user1')
    user1 = client.get('user1')
    print(user1)
    num = int(client.get('num').decode())
    lnum = pickle.loads(client.get('lnum'))
    print(num)
    print(lnum)

