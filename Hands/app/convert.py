import cv2
import os

def save_all_frames(video_path, dir_path, basename, ext='png'):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return

    os.makedirs(dir_path, exist_ok=True)
    base_path = os.path.join(dir_path, basename)

    digit = len(str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))

    n = 0

    while True:
        ret, frame = cap.read()
        if ret:
            cv2.imwrite('{}_{}.{}'.format(base_path, str(n).zfill(digit), ext), frame)
            n += 1
        else:
            return
        
save_all_frames('/usr/src/app/input/20220922_hino.mp4', '/usr/src/app/image', 'sample', 'png')

#save_all_frames('data/temp/sample_video.mp4', 'data/temp/result', 'sample_video_img')
