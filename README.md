## sampleフォルダ
TCP、UDP通信に関するコード部品です。

## udp_txt.py（UDPテキスト相互通信）
### 実行の準備
- ポート開放  
  WAN上で通信する場合は、ポート開放の設定が必要な場合が多いです。  
  各自設定をお願い致します。
  
## udp_chat_gui.py（UDPチャットプログラム（GUI））← 現在使われていません。

### 実行の準備
- 利用している外部ライブラリ  
  以下のライブラリをインストールしないと動きません。  
  [pynat](https://pypi.org/project/pynat/)  
  ⇒ ローカルIPからグローバルIPを取得するのに利用しています。  
  
- ポート開放  
  WAN上で通信する場合は、ポート開放の設定が必要な場合が多いです。  
  各自設定をお願い致します。

### 参考にしたサイト
- 受信と送信を並行に行えるクライアントの作成【Python, Tkinter, socket】  
  https://yu-nix.com/blog/2020/12/21/python-receiver-and-sender/

- Pythonによるソケットプログラミング(UDP編)  
  https://qiita.com/note-tech/items/c3e1e497d231ea1e7ca7

