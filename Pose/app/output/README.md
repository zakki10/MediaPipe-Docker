# 検出結果が出力されるディレクトリ

出力先を変更したい場合は、[`Pose/app/pose.py`](https://github.com/AO2324-00/MediaPipe-Docker/blob/main/Pose/app/pose.py) の84行目や87行目、115行目のパスを変更してください。
```python
83   # ランドマークを描画した画像を出力します。
84   cv2.imwrite('./output/annotated_image' + str(index) + '.png', annotated_image)
85
86   # ワールド座標系のランドマーク座標をテキストファイルに書き出します。
87   with open('./output/world_lamdmarls_' + str(index) + '.txt', mode='w') as file:
88      file.write(str(landmarks.pose_world_landmarks))

114  # VideoWriterを作成します。
115  video = cv2.VideoWriter('./output/annotated_video.mp4', fmt, fps, (width, height))
```