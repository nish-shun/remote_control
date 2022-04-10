import socket
import threading
from sys import argv

class App :

    # 送信先IP・ポート
    send_ip = "192.168.0.10"
    send_port = 42000

    # 受信IP・ポート
    receive_port = 42001

    #
    # コンストラクタ
    # 
    def __init__(self, ):
        # ソケット
        self.send_socket  = socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM) 
        self.receive_socket  = socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM) 
        self.receive_socket.bind((socket.gethostname(), self.receive_port))

    #
    # 受信スレッド起動
    #
    def start_receive_thread(self) :
        th_receive = threading.Thread(target=self.receive, daemon=True)
        th_receive.start()

    #
    # 受信待機
    #
    def receive(self):
        try:
            while True:
                message, client_addr = self.receive_socket.recvfrom(1024)
                message = message.decode(encoding='utf-8')
                print("You got Message:" + message)
        except:
            pass
                
    #
    # ソケットクローズ
    #
    def close_socket(self):
        self.receive_socket.shutdown(socket.SHUT_WR)
        self.receive_socket.close()
        self.send_socket.close()
        print('end...')

    #
    # 実行
    #
    def exec(self):

        # 受信サーバー起動
        self.start_receive_thread()

        # 送信テキスト入力
        while True:
            try:
                print('Input any messages, Type [end] to exit')
                message = input()
                if message != 'end':
                    self.send_socket.sendto(message.encode('utf-8'), (self.send_ip, self.send_port))
                else:
                    self.close_socket()
                    break
            except KeyboardInterrupt:
                self.close_socket()
                break

def main():
    app = App().exec()

if __name__ == "__main__":
    main()