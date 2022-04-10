import socket
import cv2
import numpy as np

# 接続情報
IP = '192.168.0.10'
PORT = 8820

# カメラ情報
D_WIDTH = 170
D_HEIGHT = 120

# ソケット
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print ('start camera')
cap = cv2.VideoCapture(0)

# FPSを落とします
# カメラが対応していないと、setがTrueを返しても変わりません。
print('FPS変更：{}'.format(cap.set(cv2.CAP_PROP_FPS, 10)))
print('FPS：{}'.format(cap.get(cv2.CAP_PROP_FPS)))

while (cap.isOpened()):
  ret, data = cap.read()
  data = cv2.resize(data, dsize=(D_WIDTH, D_HEIGHT))

  # 転送するために画像データをエンコードする -------------------------
  img_encode = cv2.imencode('.png', data)[1]
  data_encode = np.array(img_encode)
  data = data_encode.tobytes()

  # データを送る:
  sock.sendto(data,(IP, PORT))

  if cv2.waitKey(1) & 0xFF == ord('q'):
    print ("quit")
    break

# 終了処理
cap.release()
cv2.destroyAllWindows()
sock.shutdown();
sock.close();




