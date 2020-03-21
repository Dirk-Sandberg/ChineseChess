# Chinese Chess / Xiangqi Online
## Features
- Accounts through Firebase Authentication
- Ranked ELO system, data held in Firebase Real-time Database
- Online multiplayer

## Screenshots

![First three screens](https://user-images.githubusercontent.com/37519914/77214771-98f99980-6ade-11ea-9e1f-e3c5f9df2391.png)
![Board screenshots](https://user-images.githubusercontent.com/37519914/77214670-37d1c600-6ade-11ea-8c47-1f1844fbc4b8.png)


## Running this code yourself
_This is assuming you are more interested in the internals of the game rather than playing the game, as you can simply download the app to play the game._

> If you want to clone or fork this repo, you will be missing a file, `server_ip.txt`, which contains the ip address of your server. Your server would be a computer that is running `communications/server.py`

If you want to connect to your own server after maybe forking this project, you have two options:
1. Hosting a local server locally
2. Hosting a server through a cloud service

### Running the server 
#### How to set up the server on your local machine
1. Clone this repository using `git clone https://github.com/Dirk-Sandberg/ChineseChess.git`
2. Change into the projects directory using `cd ChineseChess`
3. Create a file named `server_ip.txt` and put `127.0.0.1` inside. This means your clients will connect to localhost -- your own computer.
4. Install the required modules for the server using `python3 -m pip install -r communications/requirements.txt`.
5. Open a terminal and run `python3 communications/server.py`.

At this point you're ready to connect to your server.

#### How to set up the server on Google Compute Engine (part of Google Cloud Platform)
1. Create an account on [Google Cloud Platform](https://cloud.google.com/)
2. Create a new Google Compute Engine instance (select the free tier for everything so you don't get charged).
3. Create a new firewall rule for your instance that allows TCP communication on port 65432.
4. Write the instance's public ip address in the `server_ip.txt` file of your clients.
5. SSH into your instance and clone this repository.
6. Change into the cloned directory. 
7. Install the required modules for the __server__ using `python3 -m pip install -r communications/requirements.txt`.
8. Type `screen` into your terminal. This is to make it so your server runs even when you close the SSH terminal.
9. Type `python3 communications/server.py`. You can now close the SSH terminal.
10. When you log back into your SSH terminal, you can kill the server by typing `screen -r` which restores the screen you ran earlier. Then just `ctrl-c` to end the process.

At this point you're ready to connect to your server.
---
### Running the clients
You can skip steps 1, 2, and 3 here if you've already done them from above.
1. Clone this repository using `git clone https://github.com/Dirk-Sandberg/ChineseChess.git`
2. Change into the projects directory using `cd ChineseChess`
3. Create a file named `server_ip.txt` and put `127.0.0.1` inside. This means your clients will connect to localhost -- your own computer.
4. Install the required modules for the __client__ using `python3 -m pip install -r requirements.txt` (tested on Mac OSX, you may need to follow instructions to [install kivy](https://kivy.org/doc/stable/gettingstarted/installation.html) based on your OS).
5. Bring your first client/player up with by running `python3 main.py`.
6. Bring your second client/player up with by running `python3 main.py`.

> Please note that account info (nickname and elo) is saved on the client's device. If you run two clients on the same device, you will run into some ~~bugs~~ interesting features when winning/losing a match. 

---
## Why did I make this game? 
I play chinese chess in person with a couple friends, but we didn't have a way to play when we weren't physically connected.

I also wanted to create an app with a client/server architecture and teach myself how to host the server online. I chose to host the server using a Google Compute Engine instance.

This app is currently being uploaded to the App Store and Google Play Store. Check back for the download links!
