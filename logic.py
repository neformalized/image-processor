import loader
import media_tools
import os, time

from prompts import prompts

from bridge import BridgeVision, transcribe
from encoder import encode_image, encode_video, encode_audio

from PIL import Image

import cv2

class Logic:
    
    def __init__(self):
        
        self.bridgeVision = BridgeVision(
            api_key="sk-ws-djI.ppYXF88vDUGfrRdNYMEahPe8v8oWgXFI6EFeSl3UURzzKfZpPBZKI2NoRYvxWG65cXzczPgxDY6vXnJwMmzqdXZRUclRiiRsqFSuOimbLZY9Redig9oVWrcDAMF9Z3Jx.MEUCIQCrepaRUcbIdIRxztaw1iV9sqV_rjIO2nyp2ZeY6qXfPQIgU6pCzmuNalUVlvVHA3KltXOA-D5UtoWRTcPelLCzih4",
            base_url="https://ws-k0ntb2rbsbs2h1rv.eu-central-1.maas.aliyuncs.com/compatible-mode/v1"
        )
    #

    def pipeline_image(self, response, usage, path_image):
        
        image = encode_image(path_image)
        
        res = self.bridgeVision.infer_image(
            image=image,
            prompt=prompts["is_igaming_vision"],
        )
        
        result = res["result"]
        usage.append(res["usage"])
        
        if result["confidence"] >= 0.8:
            response["igaming"]["isIgaming"] = True
            response["igaming"]["explicit"] = True
            response["igaming"]["confidence"] = result["confidence"]
        #

        if not response["igaming"]["isIgaming"]:

            res = self.bridgeVision.infer_image(
                image=image,
                prompt=prompts["is_implicit_igaming_vision"],
            )
            
            result = res["result"]
            usage.append(res["usage"])
            
            if result["confidence"] >= 0.5:
                response["igaming"]["isIgaming"] = True
                response["igaming"]["explicit"] = False
                response["igaming"]["confidence"] = result["confidence"]
            #
        #
        
        if not response["igaming"]["isIgaming"]: return
        
        res = self.bridgeVision.infer_image(
            image=image,
            prompt=prompts["game_type"],
        )
        
        result = res["result"]
        usage.append(res["usage"])
        
        response["type"]["type"] = result["game_type"]
        response["type"]["confidence"] = result["confidence"]

        res = self.bridgeVision.infer_image(
            image=image,
            prompt=prompts["game_title"],
        )
        
        result = res["result"]
        usage.append(res["usage"])
        
        response["game"]["game"] = result["game_title"]
        response["game"]["confidence"] = result["confidence"]

        res = self.bridgeVision.infer_image(
            image=image,
            prompt=prompts["ocr"],
        )
        
        result = res["result"]
        usage.append(res["usage"])

        response["ocr"]["text"] = result["text"]
        response["ocr"]["confidence"] = result["confidence"]
    #

    def pipeline_video(self, response, usage, path_video):
        
        if media_tools.has_audio(path_video):
            
            transcribed = transcribe(encode_audio(media_tools.extract_audio_bytes(path_video)))
            
            if bool(transcribed.strip()):
                
                self.sub_pipeline_transcribed(response, usage, transcribed)
            #
        #
        
        self.sub_pipeline_video(response, usage, path_video)
        
        #
        
        return response
    #

    def sub_pipeline_transcribed(self, response, usage, transcribed):
        
        res = self.bridgeVision.infer_text(
            text=transcribed,
            prompt=prompts["is_igaming_audio"],
        )
        
        result = res["result"]
        usage.append(res["usage"])
        
        if result["confidence"] >= 0.8:
            response["igaming"]["isIgaming"] = True
            response["igaming"]["explicit"] = True
            response["igaming"]["confidence"] = result["confidence"]
        #

        if not response["igaming"]["isIgaming"]:

            res = self.bridgeVision.infer_text(
                text=transcribed,
                prompt=prompts["is_implicit_igaming_audio"],
            )
            
            result = res["result"]
            usage.append(res["usage"])

            if result["confidence"] >= 0.5:
                response["igaming"]["isIgaming"] = True
                response["igaming"]["explicit"] = False
                response["igaming"]["confidence"] = result["confidence"]
            #
        #
        
        if not response["igaming"]["isIgaming"]: return
        
        #
        
        res = self.bridgeVision.infer_text(
            text=transcribed,
            prompt=prompts["game_type"],
        )
        
        result = res["result"]
        usage.append(res["usage"])

        response["type"]["type"] = result["game_type"]
        response["type"]["confidence"] = result["confidence"]

        res = self.bridgeVision.infer_text(
            text=transcribed,
            prompt=prompts["game_title"],
        )
        
        result = res["result"]
        usage.append(res["usage"])

        response["game"]["game"] = result["game_title"]
        response["game"]["confidence"] = result["confidence"]
        
        response["ocr"]["text"] = transcribed
        response["ocr"]["confidence"] = 1.
    #

    def sub_pipeline_video(self, response, usage, path_video):
        
        video = encode_video(path_video)
        
        if not response["igaming"]["isIgaming"]:
            
            res = self.bridgeVision.infer_video(
                video=video,
                prompt=prompts["is_igaming_vision"],
            )
            
            result = res["result"]
            usage.append(res["usage"])
            
            if result["confidence"] >= 0.8:
                response["igaming"]["isIgaming"] = True
                response["igaming"]["explicit"] = True
                response["igaming"]["confidence"] = result["confidence"]
            #
        #

        if not response["igaming"]["isIgaming"]:

            res = self.bridgeVision.infer_video(
                video=video,
                prompt=prompts["is_implicit_igaming_vision"],
            )
            
            result = res["result"]
            usage.append(res["usage"])

            if result["confidence"] >= 0.5:
                response["igaming"]["isIgaming"] = True
                response["igaming"]["explicit"] = False
                response["igaming"]["confidence"] = result["confidence"]
            #
        #
        
        if not response["igaming"]["isIgaming"]: return

        if not bool(response["type"]["type"]):
            
            res = self.bridgeVision.infer_video(
                video=video,
                prompt=prompts["game_type"],
            )
            
            result = res["result"]
            usage.append(res["usage"])
            
            response["type"]["type"] = result["game_type"]
            response["type"]["confidence"] = result["confidence"]
        #

        if not bool(response["game"]["game"]):
            
            res = self.bridgeVision.infer_video(
                video=video,
                prompt=prompts["game_title"],
            )
            
            result = res["result"]
            usage.append(res["usage"])

            response["game"]["game"] = result["game_title"]
            response["game"]["confidence"] = result["confidence"]
        #

        if not bool(response["ocr"]["text"]):
            
            res = self.bridgeVision.infer_video(
                video=video,
                prompt=prompts["ocr"],
            )
            
            result = res["result"]
            usage.append(res["usage"])

            response["ocr"]["text"] = result["text"]
            response["ocr"]["confidence"] = result["confidence"]
        #
    #

    def work(self, link: str):
        
        response = {
            "mediaId": "",
            "igaming": {
                "isIgaming": False,
                "explicit": False,
                "confidence": 0.0
            },
            "type": {
                "type": "",
                "confidence": 0.0
            },
            "game": {
                "game": "",
                "confidence": 0.0
            },
            "ocr": {
                "text": "",
                "confidence": 0.0
            }
        }
        
        usage = []
        
        file, _type = loader.download_file(link)
        
        #

        if _type is None:
            
            print(f"Unknown content type for link: {link}")
            os.remove(file)
            return
        #

        if _type == "image":
            
            print(f"Image file downloaded: {file}")
                
            try:
                Image.open(file).verify()
            except Exception as e:
                print(f"Failed to open image file: {file}, error: {e}")
                os.remove(file)
                return
            #

            self.pipeline_image(response, usage, file)
        #

        if _type == "video":
            
            print(f"Video file: {file}")

            if not media_tools.video_verify(file):
                
                print(f"Video verification failed for file: {file}")
                os.remove(file)
                return
            #

            self.pipeline_video(response, usage, file)
        #
        
        os.remove(file)

        return [response, usage]
    #
#