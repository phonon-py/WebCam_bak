import tkinter as tk
from tkinter import ttk
import cv2
import PIL.Image, PIL.ImageTk
from tkinter import font
import time


# https://qiita.com/kotai2003/items/3d31528d56059c848458
class Application(tk.Frame):
    def __init__(self,master, video_source=0):
        super().__init__(master)

        self.master.geometry("1280x900")
        self.master.title("Tkinter with Video Streaming and Capture")

        # ---------------------------------------------------------
        # Font
        # ---------------------------------------------------------
        self.font_frame = font.Font( family="Meiryo UI", size=15, weight="normal" )
        self.font_btn_big = font.Font( family="Meiryo UI", size=20, weight="bold" )
        self.font_btn_small = font.Font( family="Meiryo UI", size=15, weight="bold" )

        self.font_lbl_bigger = font.Font( family="Meiryo UI", size=45, weight="bold" )
        self.font_lbl_big = font.Font( family="Meiryo UI", size=30, weight="bold" )
        self.font_lbl_middle = font.Font( family="Meiryo UI", size=15, weight="bold" )
        self.font_lbl_small = font.Font( family="Meiryo UI", size=12, weight="normal" )

        # ---------------------------------------------------------
        # Open the video source
        # ---------------------------------------------------------

        self.vcap = cv2.VideoCapture( video_source )
        self.width = self.vcap.get( cv2.CAP_PROP_FRAME_WIDTH )
        self.height = self.vcap.get( cv2.CAP_PROP_FRAME_HEIGHT )

        # ---------------------------------------------------------
        # Widget
        # ---------------------------------------------------------

        self.create_widgets()

        # ---------------------------------------------------------
        # Canvas Update
        # ---------------------------------------------------------

        self.delay = 15 #[mili seconds]
        self.update()


    def create_widgets(self):
        global input_pulldown
        
        #Frame_Camera
        self.frame_cam = tk.LabelFrame(self.master, text = 'カメラ画像', font=self.font_frame)
        self.frame_cam.pack(side='top')
        self.frame_cam.configure(width = self.width-60, height = self.height-100)
        self.frame_cam.grid_propagate(0)

        #Canvas
        self.canvas1 = tk.Canvas(self.frame_cam)
        self.canvas1.configure( width= self.width, height=self.height)
        self.canvas1.grid(column= 0, row=0,padx = 10, pady=10)

        # 部品用のフレーム
        self.frame_parts = tk.LabelFrame( self.master, text='部品名', font=self.font_frame )
        self.frame_parts.pack()
        self.frame_parts.configure( width=self.width + 30, height=120 )
        self.frame_parts.grid_propagate( 0 )


        # 部品のボタンを作成
        self.btn_slv = tk.Button(self.frame_parts, text='部品1', font=self.font_btn_big)
        self.btn_slv.configure(width = 15, height = 1, command=lambda: self.add_parts_name('部品1'))
        self.btn_slv.grid(row=0, column=0, padx=30, pady= 10)

        self.btn_drum = tk.Button(self.frame_parts, text='部品2', font=self.font_btn_big)
        self.btn_drum.configure(width = 15, height = 1, command=lambda: self.add_parts_name('部品2'))
        self.btn_drum.grid(row=0, column=1, padx=30, pady= 10)

        self.btn_d_blade = tk.Button(self.frame_parts, text='Dブレード', font=self.font_btn_big)
        self.btn_d_blade.configure(width = 15, height = 1, command=lambda: self.add_parts_name('Dブレード'))
        self.btn_d_blade.grid(row=0, column=2, padx=30, pady= 10)

        # Frame_Button
        self.frame_btn = tk.LabelFrame( self.master, text='Control', font=self.font_frame )
        self.frame_btn.pack(side="bottom")
        self.frame_btn.configure( width=self.width + 30, height=120 )
        self.frame_btn.grid_propagate( 0 )

        #Snapshot Button
        self.btn_snapshot = tk.Button( self.frame_btn, text='撮影', font=self.font_btn_big)
        self.btn_snapshot.configure(width = 15, height = 1, command=self.press_snapshot_button)
        self.btn_snapshot.grid(column=0, row=0, padx=30, pady= 10)

        # Close
        self.btn_close = tk.Button( self.frame_btn, text='閉じる', font=self.font_btn_big )
        self.btn_close.configure( width=15, height=1, command=self.press_close_button )
        self.btn_close.grid( column=1, row=0, padx=20, pady=10 )




    def update(self):
        #Get a frame from the video source
        _, frame = self.vcap.read()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))

        #self.photo -> Canvas
        self.canvas1.create_image(0,0, image= self.photo, anchor = tk.NW)

        self.master.after(self.delay, self.update)

    def add_parts_name(self, strings):
        global parts_name
        parts_name = strings

    def press_snapshot_button(self):
        # ファイル名に部品名を追加するインスタンス
        # parts_name = input_pulldown.get()
        # Get a frame from the video source
        _, frame = self.vcap.read()

        frame1 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        cv2.imwrite(parts_name + ' ' + time.strftime( "%Y-%d-%m-%H-%M-%S" ) + ".jpg",
                     cv2.cvtColor( frame1, cv2.COLOR_BGR2RGB ) )

    def press_close_button(self):
        self.master.destroy()
        self.vcap.release()





def main():
    root = tk.Tk()
    app = Application(master=root)#Inherit
    app.mainloop()

if __name__ == "__main__":
    main()

