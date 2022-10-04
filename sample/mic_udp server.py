# -*- coding: utf-8 -*
import pyaudio
import socket

def main():

    # 受信IP・ポート
    receive_port = 42001

    #PyAudio設定
    fmt = pyaudio.paInt16  # 音声のフォーマット
    ch = 1              # チャンネル1(モノラル)
    sampling_rate = 44100 # サンプリング周波数
    chunk = 2**11       # チャンク（データ点数）
    audio = pyaudio.PyAudio()
    index = 1 # 録音デバイスのインデックス番号（デフォルト1）

    # ソケット
    receive_socket  = socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM)
    receive_socket.bind((socket.gethostname(), receive_port))

    # 再生処理
    out_stream = audio.open(format=fmt,
                        channels=ch,
                        rate=sampling_rate,
                        output=True)

    print("waiting...")
    while True:
        try:
            data, client_addr = receive_socket.recvfrom(8192)
            out_stream.write(data)
        except KeyboardInterrupt:
            receive_socket.close()
            break

    receive_socket.close()
    out_stream.stop_stream()
    out_stream.close()
    audio.terminate()

if __name__ == '__main__':
    main()
