import unittest
import asyncio
import jwt, datetime, time
import app.config as config


async def main():
    # Schedule three calls *concurrently*:
    await asyncio.gather(
        factorial("A", 2),
        factorial("B", 3),
        factorial("C", 4),
    )

async def factorial(name, number):
    f = 1
    for i in range(2, number + 1):
        print(f"Task {name}: Compute factorial({i})...")
        await asyncio.sleep(1)
        f *= i
    print(f"Task {name}: factorial({number}) = {f}")

class ZjjTesst(unittest.TestCase):

    def test1(self):
        asyncio.run(main())


    def test2(self):
        expire_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=5)
        payload = {
            'exp': expire_time,
            'iat': datetime.datetime.utcnow(),
            'data': {'hhh': 123},
        }
        encoded = jwt.encode(payload, config.SECRET_KEY, algorithm='HS256')
        token = str(encoded, encoding='ascii')
        print('token encoded: '+token)
        time.sleep(5.5)
        try:
            payload1 = jwt.decode(token, config.SECRET_KEY, algorithms='HS256')
            print('time is: '+str(int(time.time())))
            print('token decoded:')
            print(payload1)
        except jwt.ExpiredSignatureError:

            print('token expired!')

