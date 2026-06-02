import requests
import tempfile
import magic
from pathlib import Path

def download_file(url: str) -> Path:

    r = requests.get(url, timeout=30)
    r.raise_for_status()

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".bin")
    tmp.write(r.content)
    tmp.close()
    
    mime = magic.from_file(tmp.name, mime=True)
    _type = None
    
    if mime.startswith("image/"):
        
        _type = "image"
    if mime.startswith("video/"):
        
        _type = "video"
    #
    
    return Path(tmp.name), _type
#