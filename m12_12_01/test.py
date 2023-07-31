from jose import jwt

# дані для заповнення токена
payload = {"sub": "1234567890", "name": "John Doe"}

# створення токена з симетричним ключем
encoded = jwt.encode(payload, "secret_key", algorithm='HS256')
print(encoded)

# перевірка токена
decoded = jwt.decode(encoded, "secret_key", algorithms=['HS256'])
print(decoded)
