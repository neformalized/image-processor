import base64
import cv2
import numpy as np
from PIL import Image

def encode_audio(audio_bytes: bytes) -> str:
    
    return base64.b64encode(audio_bytes).decode("utf-8")
#

def encode_video(path: str) -> list:
    
    video = cv2.VideoCapture(path)
    
    fps = video.get(cv2.CAP_PROP_FPS)
    
    result = list()
    
    while True:
    
        success, frame = video.read()
        
        if not success: break
        
        frame_number = int(video.get(cv2.CAP_PROP_POS_FRAMES))
    
        if frame_number % int(fps * 3) == 0:
        
            _, buffer = cv2.imencode(
                ".jpg",
                cv2.resize(frame, (480, 360)),
                [int(cv2.IMWRITE_JPEG_QUALITY), 50]
            )
        
            result.append(base64.b64encode(buffer).decode('utf-8'))
        #
    #
    
    video.release()
    
    return result
#

def encode_image(path: str) -> str:
    
    image = cv2.imread(path)
    
    if image is None:
        
        image = cv2.cvtColor(
            np.array(Image.open(path)),
            cv2.COLOR_RGB2BGR
        )
    #
    
    image = cv2.resize(image, (480, 360))
    
    _, buffer = cv2.imencode(
        ".jpg",
        image,
        [int(cv2.IMWRITE_JPEG_QUALITY), 50]
    )

    return base64.b64encode(buffer).decode("utf-8")
#