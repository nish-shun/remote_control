import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 8890))  # IPとポート番号を指定します
s.listen(5)


while True:
    try:
        clientsocket, address = s.accept()
        print(f"Connection from {address} has been established!")
        clientsocket.send(bytes("Welcome to the server!", 'utf-8'))
        clientsocket.close()
    except KeyboardInterrupt:
        print("catch")
        clientsocket.close()
