import socket
import tkinter as tk
from tkinter import ttk
import threading
from pynat import get_ip_info
import tkinter.font as f

#
# アプリケーション
#
class Application(tk.Frame):

    #
    # コンストラクタ
    # 
    def __init__(self):
        super().__init__()
        self.master.title("チャット")

        # 行
        self.row = 0

        # ソケット
        self.socket_me  = socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM)
        self.socket_you  = socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM)

        # ウィジェット描画
        self.create_widgets()

    #
    # ウィジェット描画
    #
    def create_widgets(self):

        #--------------------------------------------------
        # 受信フレーム
        #--------------------------------------------------
        f1 = tk.Frame(self.master, pady=10, padx=5, relief=tk.RIDGE, bd=2)
        f1.pack(side=tk.LEFT, fill=tk.Y)

        # # --- 部品定義 ------------------------------------- 
        self.me_lbl = tk.Label(f1, text="受信", font=f.Font(weight="bold"))
        self.me_lcl_lbl = tk.Label(f1, text="■あなたのローカルIPアドレス")
        self.me_lcl_ip_lbl = tk.Label(f1,text="IPアドレス")
        self.me_lcl_ip_inpt = tk.Entry(f1,textvariable=self.getIp(), state='readonly')
        self.me_lcl_pt_lbl = tk.Label(f1,text="ポート番号")
        self.me_lcl_pt_inpt = tk.Entry(f1,textvariable=tk.StringVar())
        self.me_glb_lbl = tk.Label(f1, text="■あなたのグローバルIPアドレス")
        self.me_glb_ip_lbl = tk.Label(f1,text="IPアドレス")
        self.me_glb_ip_inpt = tk.Entry(f1,textvariable="", state='readonly')
        self.me_glb_pt_lbl = tk.Label(f1,text="ポート番号")
        self.me_glb_pt_inpt = tk.Entry(f1,textvariable=tk.StringVar(), state='readonly')
        self.me_nw_stt_btn = tk.Button(f1,text="UDPサーバ起動",command=self.start_server_thread)
        self.me_msg_dsp_lbl = tk.Label(f1, text="■受信メッセージ")
        self.me_msg_dsp_txt = tk.Text(f1, bg="#f0f0f0", height=6, width=32 )

        # # --- レイアウト ------------------------------------- 
        self.me_lbl.grid(row=self.rowInc(), column=0, sticky=tk.W)
        self.me_lcl_lbl.grid(row=self.rowInc(True), column=0, columnspan=2, sticky=tk.W)
        self.me_lcl_ip_lbl.grid(row=self.rowInc(True), column=0, sticky=tk.W)
        self.me_lcl_ip_inpt.grid(row=self.rowInc(), column=1, sticky=tk.EW)
        self.me_lcl_pt_lbl.grid(row=self.rowInc(True), column=0, sticky=tk.W)
        self.me_lcl_pt_inpt.grid(row=self.rowInc(), column=1, sticky=tk.EW)
        self.me_glb_lbl.grid(row=self.rowInc(True), column=0, columnspan=2, sticky=tk.W)
        self.me_glb_ip_lbl.grid(row=self.rowInc(True), column=0, sticky=tk.W)
        self.me_glb_ip_inpt.grid(row=self.rowInc(), column=1, sticky=tk.EW)
        self.me_glb_pt_lbl.grid(row=self.rowInc(True), column=0, sticky=tk.W)
        self.me_glb_pt_inpt.grid(row=self.rowInc(), column=1, sticky=tk.EW)
        self.me_nw_stt_btn.grid(row=self.rowInc(True), column=0, columnspan=2, sticky=tk.EW)
        self.me_msg_dsp_lbl.grid(row=self.rowInc(True), column=0, columnspan=2, sticky=tk.W)
        self.me_msg_dsp_txt.grid(row=self.rowInc(True), column=0, columnspan=2, sticky=tk.NSEW)

        #--------------------------------------------------
        # 送信フレーム
        #--------------------------------------------------
        f2 = tk.Frame(self.master, pady=10, padx=5, relief=tk.RIDGE, bd=2)
        f2.pack(side=tk.LEFT, fill=tk.Y)

        # # --- 部品定義 ------------------------------------- 
        # # 相手
        self.you_lbl = tk.Label(f2, text="相手", font=f.Font(weight="bold"))
        self.you_lg_lbl = tk.Label(f2, text="■相手のIPアドレス")
        self.you_ip_lbl = tk.Label(f2,text="IPアドレス")
        self.you_ip_inpt = tk.Entry(f2,textvariable=self.getIp())
        self.you_pt_lbl = tk.Label(f2,text="ポート番号")
        self.you_pt_inpt = tk.Entry(f2,textvariable=tk.StringVar())
        self.you_msg_lbl = tk.Label(f2, text="■送信メッセージ")
        self.you_msg_inpt = tk.Text(f2, height=6, width=32 )
        self.you_msg_send_btn = tk.Button(f2,text="メッセージ送信",command=self.send)

        # # --- レイアウト ------------------------------------- 
   
        # # 相手
        self.you_lbl.grid(row=self.rowInc(True), sticky=tk.W)
        self.you_lg_lbl.grid(row=self.rowInc(True), column=0, sticky=tk.W)
        self.you_ip_lbl.grid(row=self.rowInc(True), column=0, sticky=tk.W)
        self.you_ip_inpt.grid(row=self.rowInc(), column=1, sticky=tk.EW)
        self.you_pt_lbl.grid(row=self.rowInc(True), column=0, sticky=tk.W)
        self.you_pt_inpt.grid(row=self.rowInc(), column=1, sticky=tk.EW)
        self.you_msg_lbl.grid(row=self.rowInc(True), column=0, sticky=tk.W)
        self.you_msg_inpt.grid(row=self.rowInc(True), column=0, columnspan=2, sticky=tk.EW)
        self.you_msg_send_btn.grid(row=self.rowInc(True), column=0, columnspan=2, sticky=tk.EW)

    #
    # 行取得＋インクリメント
    #
    def rowInc(self, isInc=False):
        if (isInc) :
            self.row = self.row + 1
        return self.row
    
    #
    # ソケットからIPアドレス取得
    #
    def getIp(self):
        str_ip = tk.StringVar()
        str_ip.set(socket.gethostbyname(socket.gethostname()))
        return str_ip

    #
    # メッセージ送信
    #
    def send(self):

        # UDPメッセージ送信
        servaddr = (self.you_ip_inpt.get(), int(self.you_pt_inpt.get()))
        send_len = self.socket_you.sendto(self.you_msg_inpt.get("1.0", "end").encode('utf-8'), servaddr)
        self.you_msg_inpt.delete("1.0", "end")

        # # ③Serverからのmessageを受付開始
        # print('Waiting response from Server')
        # rx_meesage, addr = self.socket_you.recvfrom(1024)
        # print(f"[Server]: {rx_meesage.decode(encoding='utf-8')}")        

    #
    # サーバスレッド起動
    #
    def start_server_thread(self) :
        self.th_server = threading.Thread(target=self.start_server, daemon=True)
        self.th_server.start()

    #
    # サーバ起動
    #
    def start_server(self):

        # UDPサーバ起動
        locaaddr = (self.me_lcl_ip_inpt.get(), int(self.me_lcl_pt_inpt.get()))
        self.socket_me.bind(locaaddr)

        # グローバルIPアドレスの自動入力
        topology, ext_ip, ext_port = get_ip_info(source_ip=self.me_lcl_ip_inpt.get(),source_port=int(self.me_lcl_pt_inpt.get()),stun_host="stun.l.google.com",stun_port=19302,sock=self.socket_me)
        self.me_glb_ip_inpt["state"] = tk.NORMAL
        self.me_glb_pt_inpt["state"] = tk.NORMAL
        self.me_glb_ip_inpt.insert(0, ext_ip)
        self.me_glb_pt_inpt.insert(0, ext_port)
        self.me_glb_ip_inpt["state"] = tk.DISABLED
        self.me_glb_pt_inpt["state"] = tk.DISABLED

        while True:
            try :
                # Clientからのmessageの受付開始
                print('Waiting message')

                message, cli_addr = self.socket_me.recvfrom(1024)
                message = message.decode(encoding='utf-8')

                #受信メッセージのセット
                self.me_msg_dsp_txt["state"] = tk.NORMAL
                self.me_msg_dsp_txt.insert("end", message)
                self.me_msg_dsp_txt["state"] = tk.DISABLED
                
                # Clientが受信待ちになるまで待つため
                # time.sleep(1)

                # # Clientへ受信完了messageを送信
                # print('Send response to Client')
                # self.socket_me.sendto('Success to receive message'.encode(encoding='utf-8'), cli_addr)

            except KeyboardInterrupt:
                self.socket_me.close()
                break

    #
    # サーバ停止
    #
    def close_socket(self):
        self.socket_me.close();
        self.socket_you.close();

#
# 実行
#
def main():
    app = Application()
    app.mainloop()
    app.close_socket();

main()
