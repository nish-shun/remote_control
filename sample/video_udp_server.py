import socket
from telnetlib import IP
import numpy as np
import cv2

# 接続情報
IP = '192.168.0.10'
PORT = 8820
BUF = 100000

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind((IP, PORT))

while True :
  data, addr = udp.recvfrom(BUF)

  # 画像データをデコードする
  narray = np.frombuffer(data, dtype='uint8')
  data = cv2.imdecode(narray, 1)

  # 表示
  cv2.imshow('サーバー',data)

  if cv2.waitKey(1) & 0xFF == ord('q'):
    print ("quit")
    break

# 終了処理
udp.close();
cv2.destroyAllWindows()


