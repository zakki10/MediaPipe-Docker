# MediaPipe Hands

- [公式資料](https://google.github.io/mediapipe/solutions/hands.html)
- [使用イメージ](https://hub.docker.com/r/ao2324/mediapipe)

## 始め方
1. Handsディレクトリ配下のファイルとディレクトリを自身の環境に用意します。
```bash
$ git clone https://github.com/AO2324-00/MediaPipe-Docker.git
```
1. [`./app/hands.py`](https://github.com/AO2324-00/MediaPipe-Docker/blob/main/Hands/app/hands.py) の30行目や80行目を編集して、処理を行いたいファイルを指定します。
```py
30  IMAGE_FILES = ["./example.png"] # 画像のファイルパスを配列に格納して下さい。

80  VIDEO_FILE = "./example.mp4" # 動画のファイルパスを入力して下さい。
```
3. CLIにてHandsディレクトリ内に移動して `docker-compose up` コマンドを実行します。
```bash
$ cd ./MediaPipe-Docker/Hands/
$ docker-compose up
```
4. `./app/output` ディレクトリに結果が出力されます。