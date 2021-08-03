# coding: utf-8
# author: Taichi Hosoi
# usage : python [img_dir] coordinate_clicker.py

import cv2
import glob
import os
import re
import sys

class mouseParam:
    def __init__(self, input_img_name):
        # マウス入力用のパラメータ
        self.mouseEvent = {"x": None, "y": None, "event": None, "flags": None}
        # マウス入力の設定
        cv2.setMouseCallback(input_img_name, self.__CallBackFunc, None)
    # コールバック関数
    def __CallBackFunc(self, eventType, x, y, flags, userdata):
        self.mouseEvent["x"] = x
        self.mouseEvent["y"] = y
        self.mouseEvent["event"] = eventType
        self.mouseEvent["flags"] = flags
    # マウス入力用のパラメータを返すための関数
    def getData(self):
        return self.mouseEvent
    # マウスイベントを返す関数
    def getEvent(self):
        return self.mouseEvent["event"]
    # マウスフラグを返す関数
    def getFlags(self):
        return self.mouseEvent["flags"]
    # xの座標を返す関数
    def getX(self):
        return self.mouseEvent["x"]
    # yの座標を返す関数
    def getY(self):
        return self.mouseEvent["y"]
    # xとyの座標を返す関数
    def getPos(self):
        return (self.mouseEvent["x"], self.mouseEvent["y"])


if __name__ == "__main__":
    # ファイルのパスを取得
    _filelist = glob.glob(sys.argv[1]+"/*")
    # ファイルの名前をソートする
    filelist = sorted(_filelist)
    #  対象の画像拡張子を決めておく
    extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']

    # 画像の拡張子以外のものを全て除く
    for i, file in enumerate(filelist):
        if not str(os.path.splitext(file)[1]) in extensions:
            print("pop: " + str(i), file)
            filelist.pop(i)

    filelist = sorted(filelist)
    print("filelist:", filelist, "\n")
    maxi = len(filelist)

    coordinatelist = []
    pathlist = []


    _maxi = len(filelist)   # ディレクトリ内ファイルの総数
    cnt = 0                 # counter

    # ファイルの底が尽きるまでループを回し続ける
    while(cnt != maxi):
        # ファイルリストのうちインデックス番号が cnt のものを str 型で path 変数に格納
        path = str(filelist[cnt])
        # pathlist というリストにこれを格納
        pathlist.append(path)
        # 格納した path をコマンドライン表示
        print(path+" ", end='')
        # 通し番号をコマンドライン表示
        print(int(cnt), "", end="")

        # 入力画像読み込み
        read = cv2.imread(path)
        # 表示するWindow名
        window_name = "annotation window"
        # 入力画像の表示
        cv2.namedWindow(window_name, flags= cv2.WINDOW_GUI_NORMAL)
        cv2.resizeWindow(window_name, 960, 540)
        cv2.imshow(window_name, read)
        # コールバックの設定
        mouseData = mouseParam(window_name)

        # position = set()
        position = 0
        while True:
            cv2.waitKey(1)
            # 左クリックがあったら表示
            if mouseData.getEvent() == cv2.EVENT_LBUTTONDOWN:
                pos = mouseData.getPos()
                position = pos
            # 右クリックがあったら終了
            elif mouseData.getEvent() == cv2.EVENT_RBUTTONDOWN:
                break

        # # 取得した座標を tmp 変数に格納する
        # tmp = position
        # # coordinatelist というリストにこれを追加
        # coordinatelist.append(tmp)
        # # coordinatelist に入れたものから"，"を削除する
        # coordinatelist[cnt] = re.sub(r'[{(,)}]','',str(coordinatelist[cnt]))
        # # 座標データを出力
        # print(coordinatelist[cnt], end='')
        #
        # cv2.destroyAllWindows()
        # print(" Annotated ")
        # cnt += 1

        # coordinatelist に入れたものから"，"を削除する
        position = re.sub(r'[{(,)}]','',str(position))
        # 座標データを出力
        print(position, end='')

        # 座標が格納されていれば，ファイル書き込み
        i_list = position.split()
        if len(i_list) == 2:
            with open('coordinate.txt', mode='a') as f:
                f.write(path + ' ' + str(position) + '\n')
                f.close()
        elif len(i_list) == 1:
            # アノテーション対象がなかった場合のファイルを書き込む
            file = "non_used_files.txt"
            fileobj = open(file, "a", encoding="utf_8")
            fileobj.write(path + "\n")
            fileobj.close()

        cv2.destroyAllWindows()
        print(" Annotated ")
        cnt += 1

    else:
        # path = "/home/taichi/ピクチャ/sukinahito.jpeg"
        # img = cv2.imread(path)
        # height = img.shape[0]
        # width = img.shape[1]
        # img2 = cv2.resize(img, (int(width * 0.3), int(height * 0.3)))
        # window_name = "gohoubi window"
        # cv2.imshow(window_name, img2)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        print('\nFinished')