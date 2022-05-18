import numpy as np
import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

'''
背景のマスク処理を行う関数。
Arguments
 - image:     入力画像
 - landmarks: ランドマークの推定結果
Return
 - ランドマークを重ねた画像
'''
def mask_background(image, landmarks, BG_COLOR=(192, 192, 192)):
    masked_image = image.copy()
    condition = np.stack((landmarks.segmentation_mask,) * 3, axis=-1) > 0.1
    bg_image = np.zeros(image.shape, dtype=np.uint8)
    bg_image[:] = BG_COLOR
    masked_image = np.where(condition, masked_image, bg_image)
    return masked_image

'''
入力画像上にランドマークを重ねた画像を生成する関数。
Arguments
 - image:     入力画像
 - landmarks: ランドマークの推定結果
Return
 - ランドマークを重ねた画像
'''
def draw_landmarks(image, landmarks):
    annotated_image = image.copy()
    mp_drawing.draw_landmarks(
        annotated_image,
        landmarks.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
    )
    return annotated_image

'''
=== 画像の場合 ================================================
'''
IMAGE_FILES = [] # 画像のファイルパスを配列に格納して下さい。

with mp_pose.Pose(
    static_image_mode = True,       # 単体の画像かどうか(Falseの場合は入力画像を連続したものとして扱います)。
    model_complexity = 2,           # 姿勢のランドマークモデルの複雑さ(0, 1 or 2)。
    enable_segmentation = True,     # 姿勢のランドマークに加えて、セグメンテーションマスク(背景のマスク)を生成するか。
    min_detection_confidence = 0.5  # 検出が成功したと見なされるための最小信頼値(0.0 ~ 1.0)。
) as pose:
    # IMAGE_FILESの画像を一枚ずつ処理します。
    for index, file in enumerate(IMAGE_FILES):

        # BGR画像をRGBに変換します。
        image = cv2.cvtColor(cv2.imread(file), cv2.COLOR_BGR2RGB)
        
        # 画像からランドマークを推定します。
        landmarks = pose.process(image)
        '''
            landmarks.pose_landmarks
             - xとyはそれぞれ画像の幅と高さで[0.0, 1.0]に正規化された座標データ(zはxと同じスケーリングで奥行を表しています)
            landmarks.pose_world_landmarks
             - 腰の中心を原点とするメートル単位の実世界3次元座標データ
            landmarks.segmentation_mask
             - enable_segmentationがtrueに設定されている場合にのみ予測される、出力されるセグメンテーションマスク
        '''

        # ランドマークが推定できていない場合はスキップします。
        if not landmarks.pose_landmarks:
            continue

        # 画像の背景をマスクします。
        masked_image = mask_background(image, landmarks)

        # 画像に姿勢のランドマークを描画します。
        annotated_image = draw_landmarks(masked_image, landmarks)

        # RGB画像をBGRに変換します。
        annotated_image = cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR)

        # ランドマークを描画した画像を出力します。
        cv2.imwrite('./output/annotated_image_' + str(index) + '.png', annotated_image)

        # ワールド座標系のランドマーク座標をテキストファイルに書き出します。
        with open('./output/world_lamdmarls_' + str(index) + '.txt', mode='w') as file:
            file.write(str(landmarks.pose_world_landmarks))


'''
=== 動画の場合 ================================================
'''
VIDEO_FILE = "" # 動画のファイルパスを入力して下さい。

cap = cv2.VideoCapture(VIDEO_FILE)

with mp_pose.Pose(
    static_image_mode = False,      # 単体の画像かどうか(Falseの場合は入力画像を連続したものとして扱います)。
    min_detection_confidence = 0.5, # 検出が成功したと見なされるための最小信頼値(0.0 ~ 1.0)。
    min_tracking_confidence = 0.5   # 前のフレームからランドマークが正常に追跡されたとみなされるための最小信頼度(0.0 ~ 1.0)。
) as pose:

    # 動画サイズ取得します。
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # フレームレート取得します。
    fps = cap.get(cv2.CAP_PROP_FPS)

    # フォーマット指定します。
    fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

    # VideoWriterを作成します。
    video = cv2.VideoWriter('./output/annotated_video.mp4', fmt, fps, (width, height))

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            break

        # パフォーマンスを向上させるために、画像を書き込みを不可にして参照渡しとします。
        image.flags.writeable = False

        # BGR画像をRGBに変換します。
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # 動画の１フレーム(画像)からランドマークを推定します。
        landmarks = pose.process(image)
        '''
            landmarks.pose_landmarks
             - xとyはそれぞれ画像の幅と高さで[0.0, 1.0]に正規化された座標データ(zはxと同じスケーリングで奥行を表しています)
            landmarks.pose_world_landmarks
             - 腰の中心を原点とするメートル単位の実世界3次元座標データ
            landmarks.segmentation_mask
             - enable_segmentationがtrueに設定されている場合にのみ予測される、出力されるセグメンテーションマスク
        '''

        # 画像への書き込みを許可します。
        image.flags.writeable = True

        # RGB画像をBGRに変換します。
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # 画像に姿勢のランドマークを描画します。
        if landmarks.pose_landmarks:
            annotated_image = draw_landmarks(image, landmarks)
        else:
            annotated_image = image

        # 動画を書き込みます。
        video.write(annotated_image)
    video.release()
cap.release()