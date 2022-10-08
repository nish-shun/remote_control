"""
This is a test program.
"""

import socket
import threading
import pyaudio
import numpy as np
import cv2

class App :
    """ App """

    # 送信先IP・ポート
    send_ip = "192.168.0.9"
    send_txt_port = 8890
    send_mic_port = 8891
    send_video_port = 8892

    # 受信ポート
    receive_txt_port = 8893
    receive_mic_port = 8894
    receive_video_port = 8895

    # PyAudio設定
    fmt = pyaudio.paInt16  # 音声のフォーマット
    ch = 1 # チャンネル1(モノラル)
    sampling_rate = 44100 # サンプリング周波数
    chunk = 2**8 # チャンク（データ点数）。大きすぎるとaudio.openでinput_overflowのエラーになる。べき指数を小さくすればいい。
    audio = pyaudio.PyAudio()
    index = 1 # 録音デバイスのインデックス番号（デフォルト1）。マイクでインデックスを指定するとエラーになる。

    # 受信VIDEO設定
    BUF = 100000

    # 送信カメラ情報
    D_WIDTH = 170
    D_HEIGHT = 120
    EXTENSION = ".png" #.jpgにしないと動かない事もあった。UDPのsend_toでエラーにならないから厄介。

    def __init__(self, ):
        """ コンストラクタ """

        # 送信ソケット
        self.send_txt_socket  = socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM)
        self.send_mic_socket  = socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM)
        self.send_video_socket  = socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM)
        # 【テキスト】受信ソケット
        self.receive_txt_socket  = socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM)
        self.receive_txt_socket.bind((socket.gethostname(), self.receive_txt_port))
        # 【音声】受信ソケット
        self.receive_mic_socket  = socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM)
        self.receive_mic_socket.bind((socket.gethostname(), self.receive_mic_port))
        # 【映像】受信ソケット
        self.receive_video_socket  = socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM)
        self.receive_video_socket.bind((socket.gethostname(), self.receive_video_port))
        # 音声インプットストリーム
        self.input_stream = self.audio.open(format=self.fmt,
                                            channels=self.ch,
                                            rate=self.sampling_rate,
                                            input=True,
                                            input_device_index = self.index,
                                            frames_per_buffer=self.chunk)
        # 音声アウトプットストリーム
        self.output_stream = self.audio.open(format=self.fmt,
                                             channels=self.ch,
                                             rate=self.sampling_rate,
                                             output=True)
        # 映像キャプチャー
        self.cap = cv2.VideoCapture(0)

    def start_threads(self) :
        """ スレッド起動 """
        th_receive_txt = threading.Thread(target=self.receive_txt, daemon=True)
        th_receive_mic = threading.Thread(target=self.receive_mic, daemon=True)
        th_receive_video = threading.Thread(target=self.receive_video, daemon=True)
        th_send_mic = threading.Thread(target=self.send_mic, daemon=True)
        th_send_video = threading.Thread(target=self.send_video, daemon=True)
        th_receive_txt.start()
        th_receive_mic.start()
        th_receive_video.start()
        th_send_mic.start()
        th_send_video.start()

    def receive_txt(self):
        """【テキスト】受信サーバ起動 """

        print("txt receive start")
        try:
            while True:
                message, client_addr = self.receive_txt_socket.recvfrom(1024)
                message = message.decode(encoding='utf-8')
                print("You got Message:" + message)
        except: # pylint: disable=bare-except
            pass

    def receive_mic(self):
        """【音声】受信サーバ起動 """

        print("mic receive start")
        try:
            while True:
                data, client_addr = self.receive_mic_socket.recvfrom(8192)
                # print("sound!")
                self.output_stream.write(data)
        except: # pylint: disable=bare-except
            pass

    def receive_video(self):
        """【映像】受信サーバ起動 """

        print("video receive start")
        try:
            while True :
                data, client_addr = self.receive_video_socket.recvfrom(self.BUF)
                # print("video!")
                # 画像データをデコードする
                narray = np.frombuffer(data, dtype='uint8')
                data = cv2.imdecode(narray, 1)
                cv2.imshow('映像', data)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print ("quit")
                    break
        except: # pylint: disable=bare-except
            pass

    def send_mic(self):
        """【音声】送信処理起動 """

        print("mic send start")
        try:
            while True:
                data = self.input_stream.read(self.chunk)
                self.send_mic_socket.sendto(data, (self.send_ip, self.send_mic_port))
        except : # pylint: disable=bare-except
            pass

    def send_video(self):
        """【映像】送信処理起動 """

        print("video send start")
        # FPSを落とします
        # カメラが対応していないと、setがTrueを返しても変わりません。
        print(f'FPS変更:{self.cap.set(cv2.CAP_PROP_FPS, 10)}')
        print(f'FPS:{self.cap.get(cv2.CAP_PROP_FPS)}')

        while (self.cap.isOpened()):
            ret, data = self.cap.read()
            data = cv2.resize(data, dsize=(self.D_WIDTH, self.D_HEIGHT))
            # 転送するために画像データをエンコードする -------------------------
            img_encode = cv2.imencode(self.EXTENSION, data)[1]
            data_encode = np.array(img_encode)
            data = data_encode.tobytes()
            # データを送る:
            self.send_video_socket.sendto(data,(self.send_ip, self.send_video_port))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print ("quit")
                break

    def close(self):
        """ クローズ処理 """

        #ソケットクローズ
        self.receive_txt_socket.shutdown(socket.SHUT_WR)
        self.receive_txt_socket.close()
        self.receive_mic_socket.shutdown(socket.SHUT_WR)
        self.receive_mic_socket.close()
        self.receive_video_socket.shutdown(socket.SHUT_WR)
        self.receive_video_socket.close()
        self.send_mic_socket.shutdown(socket.SHUT_WR)
        self.send_mic_socket.close()
        self.send_video_socket.shutdown(socket.SHUT_WR)
        self.send_video_socket.close()
        # マイクストリームクローズ
        self.input_stream.stop_stream()
        self.input_stream.close()
        self.output_stream.stop_stream()
        self.output_stream.close()
        # pyaudio
        self.audio.terminate()
        # ウィンドウクローズ
        cv2.destroyAllWindows()

        print('end...')

    def exec(self):
        """ 実行 """

        # スレッド起動
        self.start_threads()

        # 送信テキスト入力
        while True:
            try:
                print('Input any messages, Type [end] to exit')
                message = input()
                if message != 'end':
                    self.send_txt_socket.sendto(message.encode('utf-8'), (self.send_ip, self.send_txt_port))
                else:
                    self.close()
                    break
            except KeyboardInterrupt:
                self.close()
                break

def main():
    """ メイン """
    App().exec()

if __name__ == "__main__":
    main()
