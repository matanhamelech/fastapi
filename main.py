from fastapi import FastAPI, Request
# from pydantic import BaseModel
import subprocess
import uvicorn
from cryptography.fernet import Fernet

app = FastAPI()


def load_key():
    """
    Load the previously generated key
    """
    return open("secret.key", "rb").read()


def encrypt_message(message):
    """
    Encrypts a message
    """
    key = load_key()
    f = Fernet(key)
    message = message.encode()
    encrypted_message = f.encrypt(message)
    return encrypted_message


def decrypt_message(encrypted_message):
    """
    Decrypts an encrypted message
    """
    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message)
    return decrypted_message


@app.put("/download/")
async def exec_download(request: Request):
    data = await request.body()
    file_name = decrypt_message(data).decode()
    file = open(f"/home/user/fastapi/{file_name}", 'r').read()
    return encrypt_message(file)


@app.put("/upload/")
async def upload(request: Request):
    data = await request.body()
    data = decrypt_message(data).decode('unicode_escape')
    data = data.split(",")
    print(data)
    file_name = data[0]
    data.pop(0)
    content = ",".join(data)
    file = open(f"/home/user/fastapi/{file_name}", 'w')
    file.write(content)
    file.close()
    print(data)


@app.put("/regular/")
async def regular(request: Request):
    data = await request.body()
    data = decrypt_message(data).decode()
    command = data.split(" ")
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = proc.communicate()
    return encrypt_message(output.decode())


if __name__ == '__main__':
    uvicorn.run("main:app")
