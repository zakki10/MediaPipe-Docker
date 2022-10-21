import cv2
import mediapipe as mp
import numpy as np
import math

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

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

IMAGE_FILES = ['/usr/src/app/input/sample_072.png'] # 画像のファイルパスを配列に格納して下さい。

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
             - label: 左右どちらの手、score: 利き手の確率
            landmarks.multi_hand_landmarks
             - xとyはそれぞれ画像の幅と高さで[0.0, 1.0]に正規化された座標データ(zはxと同じスケーリングで奥行を表しています)
            landmarks.multi_hand_world_landmarks
             - 手のおおよその幾何学的中心を原点とするメートル単位の実世界3次元座標データ
        '''
        
        # 関節点（5, 6, 8)の角度を算出
        #a = np.array(landmarks.multi_hand_world_landmarks[5].x, landmarks.multi_hand_world_landmarks[5].y, landmarks.multi_hand_world_landmarks[5].z)
        #b = np.array(landmarks.multi_hand_world_landmarks[6].x, landmarks.multi_hand_world_landmarks[6].y, landmarks.multi_hand_world_landmarks[6].z)
        #c = np.array(landmarks.multi_hand_world_landmarks[8].x, landmarks.multi_hand_world_landmarks[8].y, landmarks.multi_hand_world_landmarks[8].z)
        #print(a)
        #print(b)
        #print(c)
        
        #print(np.round(landmarks.multi_hand_world_landmarks, 4))
        #print(landmarks.multi_hand_world_landmarks.landmark[5])

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
        cv2.imwrite('./output/annotated_image_' + str(index) + '.png', annotated_image)

        # ワールド座標系のランドマーク座標をテキストファイルに書き出します。
        with open('./output/world_lamdmarks_' + str(index) + '.txt', mode='w') as file:
            file.write(str(landmarks.multi_hand_world_landmarks))
          
        #print(landmarks.multi_hand_world_landmarks.landmark[0])
        

        
        
    


        
        

