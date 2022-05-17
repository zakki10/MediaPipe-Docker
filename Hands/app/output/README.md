# 検出結果が出力されるディレクトリ

出力先を変更したい場合は、[`Hands/app/hands.py`](https://github.com/AO2324-00/MediaPipe-Docker/blob/main/Hands/app/hands.py) の73行目や76行目、105行目のパスを変更してください。
```python
72   # ランドマークを描画した画像を出力します。
73   cv2.imwrite('./output/annotated_image' + str(index) + '.png', annotated_image)
74
75   # ワールド座標系のランドマーク座標をテキストファイルに書き出します。
76   with open('./output/world_lamdmarls_' + str(index) + '.txt', mode='w') as file:
77      file.write(str(landmarks.multi_hand_world_landmarks))

104  # VideoWriterを作成します。
105  video = cv2.VideoWriter('./output/annotated_video.mp4', fmt, fps, (width, height))
```