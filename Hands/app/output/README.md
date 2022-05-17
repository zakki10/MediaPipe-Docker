# 検出結果が出力されるディレクトリ

出力先を変更したい場合は、[`Hands/app/hands.py`](https://github.com/AO2324-00/MediaPipe-Docker/blob/main/Hands/app/hands.py) の73行目や102行目のパスを変更してください。
```python
72   # ランドマークを描画した画像を出力します。
73   cv2.imwrite('./output/annotated_image' + str(index) + '.png', annotated_image)

101  # VideoWriterを作成します。
102  video = cv2.VideoWriter('./output/annotated_video.mp4', fmt, fps, (width, height))
```