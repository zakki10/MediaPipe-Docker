# MediaPipe Pose

- [公式資料](https://google.github.io/mediapipe/solutions/pose.html)
- [使用イメージ](https://hub.docker.com/r/ao2324/mediapipe)

## 始め方
1. Poseディレクトリ配下のファイルとディレクトリを自身の環境に用意します。
```bash
$ git clone https://github.com/AO2324-00/MediaPipe-Docker.git
```
2. [`./app/pose.py`](https://github.com/AO2324-00/MediaPipe-Docker/blob/main/Pose/app/pose.py) の45行目や94行目を編集して、処理を行いたいファイルを指定します。
```py
45  IMAGE_FILES = ["./example.png"] # 画像のファイルパスを配列に格納して下さい。

94  VIDEO_FILE = "./example.mp4" # 動画のファイルパスを入力して下さい。
```
3. CLIにてPoseディレクトリ内に移動して `docker-compose up` コマンドを実行します。
```bash
$ cd ./MediaPipe-Docker/Pose/
$ docker-compose up
```
4. [`./app/output`](https://github.com/AO2324-00/MediaPipe-Docker/tree/main/Pose/app/output) ディレクトリに結果が出力されます。