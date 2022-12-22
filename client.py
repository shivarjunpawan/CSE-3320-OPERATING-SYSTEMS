# NAME: SHIVARJUN UMESHA
# ID No: 1002059222
# Assignment 4 Networks 
import socket
from Crypto.Cipher import AES
import hashlib

import os
from os import path

BUFFER = 64
STREAM_BUFF = 10240
HOST = socket.gethostbyname(socket.gethostname())
PORT = 9097
ADDR = (HOST, PORT)
FORMAT = 'utf-8'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

# pip install pycryptodome
class file_crypt:
    def __init__(self, password, IV, FORMAT):
        self.key = hashlib.sha256(password.encode(FORMAT)).digest()
        self.IV = IV.encode(FORMAT)
        self.format = AES.MODE_CBC
    def pad(self, data):
        while len(data)%16 != 0:
            data = data + b" "
        return data
    def encrypt(self, file_data):
        cipher = AES.new(self.key, self.format, self.pad(self.IV))
        return cipher.encrypt(self.pad(file_data))
    def decrypt(self, file_data):
        decipher = AES.new(self.key, self.format, self.pad(self.IV))
        return decipher.decrypt(self.pad(file_data)).rstrip()

def send_action(data):
    data = data.encode(FORMAT)
    send_len = str(len(data)).encode(FORMAT)
    send_len += b' ' * (BUFFER - len(send_len))
    client.send(send_len)
    client.send(data)
def send_data(data):
    send_len = str(len(data)).encode(FORMAT)
    send_len += b' ' * (BUFFER - len(send_len))
    client.send(send_len)

    f_data_stream = bytes()
    for i in range(0, len(data) - STREAM_BUFF, STREAM_BUFF):
        f_data_stream = data[i : i + STREAM_BUFF]
        client.send(f_data_stream)
    start = int(len(data)/STREAM_BUFF)*STREAM_BUFF 
    f_data_stream = data[start : len(data)]
    client.send(f_data_stream)
def receive_data(file):
    f_data = client.recv(BUFFER)
    print(f"Data size: {f_data}")
    data_len = f_data.decode(FORMAT)  #   determine size of file name
    if data_len:
        data_len = int(data_len)
        if data_len == -1:
            print(f"{file} is not on the server!")
            return
        data = bytes()
        for i in range(0, data_len - STREAM_BUFF, STREAM_BUFF):
            data += client.recv(STREAM_BUFF)
        start = int(data_len%STREAM_BUFF)
        data += client.recv(start)
        with open(file, 'wb') as f:
            f.write(data)
    decrypted_data = crypt.decrypt(data)
    with open(file, 'wb') as f:
        f.write(decrypted_data)
    print("Received Successfully")
    
key = input("Enter a key for AES encryption: ")
crypt = file_crypt(key, "IV123", FORMAT)
while True:
    inp = input("Send/Receive/Quit{S/R/Q}: ")
    if inp.upper() == "S":
        inp = input("File: ")
        if path.exists(inp):
            send_action("!STORE_FILE!")
            with open(inp, "rb") as f:
                file_data = f.read()
            send_data(crypt.encrypt(inp.encode(FORMAT)))
            send_data(crypt.encrypt(file_data))
            print("Sent Successfully")
        else:
            print("Not a file!")
    elif inp.upper() == "R":
        inp = input("File: ")
        send_action("GET_FILE")
        send_data(crypt.encrypt(inp.encode(FORMAT)))
        receive_data(inp)
    elif inp.upper() == "Q":
        send_action("DISCONNECT")
        break
    else:
        print("Invalid Input!")
