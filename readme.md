## 1. Installation

#### Install required packages:

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv git ffmpeg
```

#### Go to projects directory

```bash
cd ~/projects
```

#### Clone repository
```bash
git clone <REPO_URL>
```
#### Enter repository folder
```bash
cd ai-media-analyzer
```
#### Create virtual environment
```bash
python3 -m venv venv
```
#### Activate virtual environment
```bash
source venv/bin/activate
```
#### Install dependencies
```bash
pip install -r requirements.txt
``` 
#### Create environment file
```bash
touch .env
```
## 2. Running the project
#### Go to project folder
```bash
cd ai-media-analyzer
```
#### Activate virtual environment
```bash
source venv/bin/activate
```
#### Run script
```bash
python main.py
```