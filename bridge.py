from openai import OpenAI
import dashscope
import json

dashscope.base_http_api_url = 'https://dashscope-intl.aliyuncs.com/api/v1'

def transcribe(audio):
    
    data = f"data:audio/mp3;base64,{audio}"
    
    messages = [
        {
            "role": "user",
            "content": [
                {"audio": data},
            ]
        }
    ]

    response = dashscope.MultiModalConversation.call(
        
        api_key="sk-ws-H.HLMYLE.aPdA.MEUCIQCMCLvP31QGrnwddi8H8Xpv3rkidp5tpNQmyMT9bMDofQIgM7PF-z8BebpQW0dW-5POk_RxXcSl7RMdIwlumL-zKEw",
        model="qwen3-asr-flash",
        messages=messages,
        result_format="message",
        asr_options={
            # "language": "zh", # Optional. If you know the language in the audio, provide this parameter to improve recognition accuracy
            "enable_lid":True,
            "enable_itn":False
        }
    )
    
    result = dict()
    
    try:
        result["result"] = response.output.choices[0].message.content[0]["text"]
    except Exception:
        result["result"] = ""
    #
    
    result["usage"] = []
    result["usage"].append("qwen3-asr-flash")
    result["usage"].append(response.usage.input_tokens)
    result["usage"].append(response.usage.output_tokens)
    
    return results
#

class BridgeVision:
    
    def __init__(self, api_key, base_url):
        
        self.client = OpenAI(
            api_key = api_key,
            base_url = base_url
        )
    #
    
    def infer_text(self, text, prompt):
        
        response = self.client.chat.completions.create(
            model="qwen3.5-plus",
            messages=[
                {
                    "role": "system",
                    "content": prompt
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
        )
        
        result = dict()
        
        result["result"] = self._json_extract(response.choices[0].message.content)
        
        result["usage"] = []
        result["usage"].append("qwen3.5-plus")
        result["usage"].append(response.usage.prompt_tokens)
        result["usage"].append(response.usage.completion_tokens)
        
        return result
    #
    
    def infer_image(self, image, prompt):
        
        response = self.client.chat.completions.create(
            model="qwen3-vl-flash",
            messages=[
                {
                    "role": "user",
                    "content": self._generate_context([image], prompt)
                }
            ]
        )
        
        result = dict()
        
        result["result"] = self._json_extract(response.choices[0].message.content)
        
        result["usage"] = []
        result["usage"].append("qwen3-vl-flash")
        result["usage"].append(response.usage.prompt_tokens)
        result["usage"].append(response.usage.completion_tokens)
        
        return result
    #
    
    def infer_video(self, video, prompt):
        
        response = self.client.chat.completions.create(
            model="qwen3-vl-flash",
            messages=[
                {
                    "role": "user",
                    "content": self._generate_context(video, prompt)
                }
            ]
        )
        
        result = dict()
        
        result["result"] = self._json_extract(response.choices[0].message.content)
        
        result["usage"] = []
        result["usage"].append("qwen3-vl-flash")
        result["usage"].append(response.usage.prompt_tokens)
        result["usage"].append(response.usage.completion_tokens)
        
        return result
    #
    
    @staticmethod
    def _generate_context(images, prompt):
        
        context = list()
        
        for image in images: context.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image}"}})
        
        context.append({"type": "text", "text": prompt})
        
        return context
    #
    
    @staticmethod
    def _json_extract(result: str) -> str:
        
        if "{" not in result or "}" not in result:
            
            return {
                "text": "unknown",
                "confidence": 0.0
            }
        #
        
        try:
            return json.loads(result[result.index("{"): result.rindex("}") + 1])
        except ValueError:
            return {
                "text": "unknown",
                "confidence": 0.0
            }
        #
    #
#