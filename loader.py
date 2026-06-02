import requests
import tempfile
import magic
import os
from pathlib import Path

def download_file(url: str) -> Path:

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".bin")
    
    #
    
    try:
        with requests.get(url, stream=True, timeout=30) as r:
            r.raise_for_status()

            downloaded = 0

            for chunk in r.iter_content(chunk_size=8192):
                
                if not chunk:
                    continue
                #
                
                tmp.write(chunk)
                downloaded += len(chunk)
                
                #
            #
        #
        
        tmp.close()

        if downloaded == 0:
            raise ValueError("Empty response")
        #
    #
    except Exception:
        
        tmp.close()
        os.remove(tmp.name)
        raise
    #
    
    mime = magic.from_file(tmp.name, mime=True)
    _type = None
    
    if mime.startswith("image/"):
        
        _type = "image"
    if mime.startswith("video/"):
        
        _type = "video"
    #
    
    return Path(tmp.name), _type
#