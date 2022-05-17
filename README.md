# MediaPipe-Docker

Dockerイメージ **[ao2324/mediapipe](https://hub.docker.com/r/ao2324/mediapipe)** は、**OpenCV**と**MediaPipe**を動かすための**Python3**環境を提供します。

```Dockerfile
FROM ao2324/mediapipe

# 作業ディレクトリを作成
WORKDIR /usr/src/app

# ホストからファイルをコピー
COPY . .

# スクリプトを実行
CMD [ "python", "./your-mediapipe-script.py" ]
```

## 関連資料
- [公式サイト](https://google.github.io/mediapipe/)
- [使用イメージ](https://hub.docker.com/r/ao2324/mediapipe)

## サンプルコード
- [Hands](/Hands)