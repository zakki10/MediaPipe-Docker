import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

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
    for hand_landmarks in landmarks.multi_hand_landmarks:
        mp_drawing.draw_landmarks(
            annotated_image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style()
        )
    return annotated_image

'''
=== 画像の場合 ================================================
'''
IMAGE_FILES = [] # 画像のファイルパスを配列に格納して下さい。

with mp_hands.Hands(
    static_image_mode = True,      # 単体の画像かどうか(Falseの場合は入力画像を連続したものとして扱います)。
    max_num_hands = 2,             # 認識する手の最大数。
    model_complexity = 1,          # 手のランドマークモデルの複雑さ(0 or 1)。
    min_detection_confidence = 0.5 # 検出が成功したと見なされるための最小信頼値(0.0 ~ 1.0)。
) as hands:
    # IMAGE_FILESの画像を一枚ずつ処理します。
    for index, file in enumerate(IMAGE_FILES):

        # MediaPipeHandsでは、入力画像は左右反転したものであると仮定して処理されます。
        # その対策として、事前に入力画像を左右反転処理を行います。
        image = cv2.flip(cv2.imread(file), 1) 

        # BGR画像をRGBに変換します。
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # 画像からランドマークを推定します。
        landmarks = hands.process(image)
        '''
            landmarks.multi_handedness
             - 利き手の推定結果
            landmarks.multi_hand_landmarks
             - xとyはそれぞれ画像の幅と高さで[0.0, 1.0]に正規化された座標データ(zはxと同じスケーリングで奥行を表しています)
            landmarks.multi_hand_world_landmarks
             - 手のおおよその幾何学的中心を原点とするメートル単位の実世界3次元座標データ
        '''

        # ランドマークが推定できていない場合はスキップします。
        if not landmarks.multi_hand_landmarks:
            continue

        # 画像上に推定したランドマークを描画します。
        annotated_image = draw_landmarks(image, landmarks)

        # 左右の反転を元に戻します。
        annotated_image = cv2.flip(annotated_image, 1)

        # RGB画像をBGRに変換します。
        annotated_image = cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR)

        # ランドマークを描画した画像を出力します。
        cv2.imwrite('./output/annotated_image' + str(index) + '.png', annotated_image)



'''
=== 動画の場合 ================================================
'''
VIDEO_FILE = "" # 動画のファイルパスを入力して下さい。

cap = cv2.VideoCapture(VIDEO_FILE)

with mp_hands.Hands(
    static_image_mode = False,    # 単体の画像かどうか(Falseの場合は入力画像を連続したものとして扱います)。
    model_complexity=0,           # 手のランドマークモデルの複雑さ(0 or 1)。
    min_detection_confidence=0.5, # 検出が成功したと見なされるための最小信頼値(0.0 ~ 1.0)。
    min_tracking_confidence=0.5   # 前のフレームからランドマークが正常に追跡されたとみなされるための最小信頼度(0.0 ~ 1.0)。
) as hands:

    # 動画サイズ取得します。
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # フレームレート取得します。
    fps = cap.get(cv2.CAP_PROP_FPS)

    # フォーマット指定します。
    fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

    # VideoWriterを作成します。
    video = cv2.VideoWriter('./output/result.mp4', fmt, fps, (width, height))

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            break

        # パフォーマンスを向上させるために、画像を書き込みを不可にして参照渡しとします。
        image.flags.writeable = False

        # BGR画像をRGBに変換します。
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # 動画の１フレーム(画像)からランドマークを推定します。
        landmarks = hands.process(image)

        # 画像への書き込みを許可します。
        image.flags.writeable = True

        # RGB画像をBGRに変換します。
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # 手が移っている場合、画像上に推定したランドマークを描画します。
        if landmarks.multi_hand_landmarks:
            annotated_image = draw_landmarks(image, landmarks)
        else:
            annotated_image = image

        # 動画を書き込みます。
        video.write(annotated_image)
    video.release()
cap.release()
