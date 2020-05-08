# Install everything necessary to run the server
# Could get this external IP and set it on firebase
# or just put this instance in a group for a load balancer

sudo apt install -y git
git clone https://github.com/Dirk-Sandberg/ChineseChess.git
git -C ChineseChess pull
sudo apt-get install -y python3-pip
sudo pip3 install -r ChineseChess/communications/requirements.txt
python3 ChineseChess/communications/server.py USERNAME PASSWORD
