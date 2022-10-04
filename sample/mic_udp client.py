# -*- coding: utf-8 -*
import pyaudio
import socket

def main():

   # 送信先IP・ポート
    send_ip = "192.168.0.9"
    send_port = 42001

    #PyAudio設定
    fmt = pyaudio.paInt16  # 音声のフォーマット
    ch = 1              # チャンネル1(モノラル)
    sampling_rate = 44100 # サンプリング周波数
    chunk = 2**11       # チャンク（データ点数）
    audio = pyaudio.PyAudio()
    index = 1 # 録音デバイスのインデックス番号（デフォルト1）

    input_stream = audio.open(format=fmt,
                        channels=ch,
                        rate=sampling_rate,
                        input=True,
                        input_device_index = index,
                        frames_per_buffer=chunk)

    # ソケット
    send_socket  = socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM)

    # 音声送信処理
    print("start...")
    while True:
        try:
            data = input_stream.read(chunk)
            send_socket.sendto(data, (send_ip, send_port))
        except KeyboardInterrupt:
            send_socket.close()
            break
    print("end...")

    # 録音終了処理
    send_socket.close()
    input_stream.stop_stream()
    input_stream.close()
    audio.terminate()

if __name__ == '__main__':
    main()
