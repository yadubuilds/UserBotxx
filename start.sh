apt update && apt upgrade -y
apt install git -y       
git clone https://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@github.com/yadubuilds/Client-Manager cm 
cd cm
git pull
python3 -m venv project-env
source project-env/bin/activate
pip install -U pip
pip install -U -r requirements.txt
pm2 start "python3 bot.py" --name cm
pm2 save

