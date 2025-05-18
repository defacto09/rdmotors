
kk
ls
ll
history 
w
sudo ps aux | grep apt
Last login: Sun May 11 12:15:27 2025 from 185.42.130.12
root@server9108:~# sudo ps aux | grep apt
root        3211  0.0  0.1  11896  5648 pts/1    S+   12:15   0:00 sudo apt upgrade -y
root        3212  0.0  0.0  11896   888 pts/2    Ss   12:15   0:00 sudo apt upgrade -y
root        3213  0.4  2.1  98136 87028 pts/2    S+   12:15   0:03 apt upgrade -y
root        7210 82.6  0.7  33164 28784 pts/0    Rs+  12:23   5:18 /usr/bin/dpkg --status-fd 41 --no-triggers --unpack --auto-deconfigure --recursive /tmp/apt-dpkg-install-iXv6dD
root        9196  0.0  0.0   7996  1212 pts/0    S+   12:29   0:00 dpkg-deb --fsys-tarfile /tmp/apt-dpkg-install-iXv6dD/130-linux-modules-5.15.0-139-generic_5.15.0-139.149_amd64.deb
root        9197  0.1  0.0   7996   160 pts/0    S+   12:29   0:00 dpkg-deb --fsys-tarfile /tmp/apt-dpkg-install-iXv6dD/130-linux-modules-5.15.0-139-generic_5.15.0-139.149_amd64.deb
root        9198  7.7  0.2  16872 10168 pts/0    S+   12:29   0:00 dpkg-deb --fsys-tarfile /tmp/apt-dpkg-install-iXv6dD/130-linux-modules-5.15.0-139-generic_5.15.0-139.149_amd64.deb
root        9200  0.0  0.0   7008  2124 pts/3    S+   12:29   0:00 grep --color=auto apt
root@server9108:~# 
sudo apt update
apt list --upgradable
do-release-upgrade
sudo reboot
sudo apt update && sudo apt upgrade -y
sudo apt update
sudo apt install coreutils
sudo dpkg --configure -a
sudo apt install python3 python3-pip -y
sudo apt install docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo docker --version
sudo apt install apt-transport-https ca-certificates curl software-properties-common -y
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt update
apt-cache policy docker-ce
sudo apt install docker-ce -y
sudo systemctl status docker
journalctl -u docker.service
docker run -d --platform linux/amd64 --name rdmotors-bot defacto092/rdmotors-bot:v1.0
docker ps -a
docker ps
docker images
docker stop rdmotors-bot
docker rm rdmotors-bot
docker run -d --platform linux/amd64 --name rdmotors-bot defacto092/rdmotors-bot:v1.0
docker ps
docker logs rdmotors-bot
docker ps
docker logs rd-motors
docker logs rdmotors-bot
docker run -d --platform linux/amd64 --name rdmotors-bot defacto092/rdmotors-bot:v1.0
docker tag pythonproject1-telegram-bot:latest defacto092/rdmotors-bot:v1.0
docker login
docker tag pythonproject1-telegram-bot:latest defacto092/rdmotors-bot:v1.0
docker images
docker push defacto092/rdmotors-bot:v1.0
docker run -d --name rdmotors-bot defacto092/rdmotors-bot:v1.0
docker ps
docker images
docker run -d --name rdmotors-bot defacto092/rdmotors-bot:v1.0
docker logs rdmotors-bot
docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
root@server9108:~# 
docker ps -a
docker start 35df9d35cd66
docker logs <container_id_or_name>
docker logs 35df9d35cd66
docker log defacto092/rdmotors-bot:v1.0
sudo systemctl restart docker
docker ps
docker run -d 35df9d35cd66
docker inspect defacto092/rdmotors-bot:v1.0 | grep Architecture
docker run -it --entrypoint /bin/bash defacto092/rdmotors-bot:v1.0
docker build --platform linux/amd64 -t defacto092/rdmotors-bot:v1.0 .
View build details: docker-desktop://dashboard/build/desktop-linux/desktop-linux/iyycw37xb72pp9ewfwp5i1cai
defacto092@Salamahas-MacBook-Air PythonProject1 % docker inspect defacto092/rdmotors-bot:v1.0 | grep Architecture
defacto092@Salamahas-MacBook-Air PythonProject1 % docker run -d --platform linux/amd64 --name rdmotors-bot defacto092/rdmotors-bot:v1.0
docker: Error response from daemon: Conflict. The container name "/rdmotors-bot" is already in use by container "e0f00ce73984a57dbb2248c25d688f5a720ffbab3fd238f49ea62fa1719b39e9". You have to remove (or rename) that container to be able to reuse that name.
Run 'docker run --help' for more information
defacto092@Salamahas-MacBook-Air PythonProject1 % docker ps
CONTAINER ID   IMAGE                         COMMAND            CREATED              STATUS              PORTS     NAMES
e0f00ce73984   34bdf167e2fa                  "python main.py"   About a minute ago   Up About a minute             rdmotors-bot
182af36a7fe2   pythonproject1-telegram-bot   "python main.py"   2 hours ago          Up 2 hours                    rdmotors_bot
defacto092@Salamahas-MacBook-Air PythonProject1 %     docker stop rdmotors-bot  # Зупиняє контейнер
docker rm rdmotors-bot    # Видаляє контейнер
docker run -d --name rdmotors-bot defacto092/rdmotors-bot:v1.0
nano ~/.ssh/config
sudo nano /etc/ssh/sshd_config
sudo systemctl restart sshd
sudo apt install tmux  # якщо не встановлено
tmux new -s mysession
docker ps
docker run -v $(pwd)/database:/app/database c6af711a03f0
docker run -v $(pwd)/database:/app/database defacto092/rdmotors-bot:v1.0
ls ./database/rdmotors.db
docker exec -it rdmotors_bot bash
ls /app/database/rdmotors.db
docker restart rdmotors_bot
docker restart defacto092/rdmotors-bot:v1.0
docker image
docker images
apt update && apt install sqlite3
sqlite3 database/rdmotors.db
find / -name "rdmotors.db" 2>/dev/null
ls -l database/rdmotors.db
cd
cd /Users/defacto092/PycharmProjects/PythonProject1
quit
q
docker-compose up --build -d
sudo apt-get purge docker-ce
sudo apt-get autoremove
sudo apt-get install docker-ce
sudo apt-cache policy docker-ce
sudo systemctl status docker
docker --version
docker run hello-world
docker ps
docker ps -a
docker images
docker login
docker ps
docker logs rdmotors-bot
docker f logs rdmotors-bot
docker -f logs rdmotors-bot
docker logs -f rdmotors-bot
docker ps
docker docker stop rdmotors-bot
docker rm rdmotors-bo
docker stop rdmotors-bot
docker rm rdmotors-bot
docker ps
docker-compose up --build -d
sudo apt update
sudo apt install docker-compose
sudo snap install docker
docker-compose up --build -d
ls
cd /Users/defacto092/PycharmProjects/PythonProject1
docker-compose up --build -d
pwd
cd /Users/defacto092/PycharmProjects/PythonProject1
cd/Users/defacto092/PycharmProjects/PythonProject1
docker logs rdmotors-bot
docker exec -it rdmotors-bot bash
ls /app/database
docker run -d --name rdmotors-bot defacto092/rdmotors-bot:v1.0
docker stop rdmotors-bot
docker rm rdmotors-bot
docker run -d --name rdmotors-bot defacto092/rdmotors-bot:v1.0
docker ps
docker logs b842ec4be1aa21bf219acf9afe22b1560177364db82e24061bce5a481a6e7091
docker run -d --platform linux/amd64 --name rdmotors-bot defacto092/rdmotors-bot:v1.0
docker ps
docker ps -a
docker run -d --platform linux/amd64 --name rdmotors-bot defacto092/rdmotors-bot:v1.0
docker run -d b842ec4be1aa
docker run -d defacto092/rdmotors-bot:v1.0
cd /Users/defacto092/PycharmProjects/PythonProject1
cd ~
ls
find / -name "main.py" 2>/dev/null
docker ps 
docker exec -t c6af711a03f0 bash
docker ps
docker logs -f c6af711a03f0
ps aux | grep python
nohup python3 main.py &
tmux kill-session -t mysession
docker logs rdmotors-bot
docker ps
docker ps -a
docker images
docker-compose up --build -d
cd /Users/defacto092/PycharmProjects/PythonProject1
cd ~
find / -name "docker-compose.yml"
cd /Users/defacto092/PycharmProjects/PythonProject1
docker inspect --format '{{.Architecture}}' rdmotors-bot
docker tag rdmotors-bot <dockerhub_username>/rdmotors-bot:v1.0
docker stop rdmotors-bot
вщслук зі
docker ps
docker images
docker pull defacto092/rdmotors-bot:v1.0
docker push defacto092/rdmotors-bot:v1.0
docker login
docker run -d --name rdmotors-bot defacto092/rdmotors-bot:v1.0
docker ps
docker logs e7e0c4b36117
docker ps
docker logs e7e0c4b36117
sudo apt update
sudo apt install tmux
tmux new-session -s mysession
python3 main.py
cd /Users/defacto092/PycharmProjects/PythonProject1
tmux new-session -s mysession
tmux ls
tmux attach-session -t mysession
tmux new-session -s mysession
docker compose up --build
docker ps
docker logs -f e7e0c4b36117
docker ps
docker exec -it e7e0c4b36117 /bin/bash
sqlite3 /app/database/rdmotors.db
ls -l /app/database/rdmotors.db
chmod 777 /app/database
ls /app
ls /app/database
sqlite3 /app/database/rdmotors.db
mkdir -p /app/database
chmod 777 /app/database
ls /app/database
sqlite3 /app/database/rdmotors.db
docker restart <container_id
docker ps
docker restart e7e0c4b36117
chmod 777 /app/database
sqlite3 /app/database/rdmotors.db
docker ps
docker run -d --name rdmotors-bot rdmotors-bot:v1.0
docker logs -f e7e0c4b36117
docker exec -it rdmotors-bot /bin/bash
docker cp rdmotors-bot:/app/database/rdmotors.db ./rdmotors.db
sqlite3 ./rdmotors.db
docker logs -f 
docker ps
docker logs -f e7e0c4b36117
docker cp rdmotors-bot:/app/database/rdmotors.db /root/rdmotors.db
mkdir -p /opt/rdmotors_data
docker exec -it rdmotors-bot bash
docker ps
docker exec -it rdmotors-bot /bin/bash
docker cp rdmotors-bot:/app/database/rdmotors.db ~/Downloads/rdmotors.db
docker cp rdmotors-bot:/app/database/rdmotors.db ~/Users/defacto092/rdmotors.db
docker cp rdmotors-bot:/app/database/rdmotors.db ./rdmotors.db
ls ~
scp root@server:/root/rdmotors.db ~/Downloads/rdmotors.db
scp root@193.169.188.220:/root/rdmotors.db ~/Downloads/rdmotors.db
mkdir -p ~/Downloads
scp root@193.169.188.220:/root/rdmotors.db /home/defacto092/Downloads/rdmotors.db
mkdir -p ~/Downloads
scp root@193.169.188.220:/root/rdmotors.db /home/defacto092/Downloads/rdmotors.db
scp root@193.169.188.220:/root/rdmotors.db /Users/defacto092/Downloads/rdmotors.db
scp root@193.169.188.220:/root/rdmotors.db /Users/defacto092/Downloads/
scp root@193.169.188.220:/root/rdmotors.db /Users/defacto092/Downloads
scp root@193.169.188.220:/root/rdmotors.db /Users/defacto092
docker exec -it rdmotors-bot /bin/bash
docker cp rdmotors-bot:/app/database/rdmotors.db /root/rdmotors.db
mkdir -p /Users/defacto092/Downloads
scp root@193.169.188.220:/root/rdmotors.db /Users/defacto092/Downloads/rdmotors.db
docker ps
sqlite3 rdmotors.db
mkdir ~/server-db
sshfs user@193.169.188.220:/path/to/db/ ~/server-db
sqlite3 ~/server-db/rdmotors.db
apt install sshfs
find / -name "rdmotors.db" 2>dev/null
cd ~
find . -name "rdmotors.db"
docker ps
docker ps                     # подивись активні контейнери
docker exec -it e7e0c4b36117 /bin/sh
find / -name "rdmotors.db"
docker cp rdmotors-bot:/app/database/rdmotors.db ~/rdmotors.db
scp root@193.169.188.220:/app/database/rdmotors.db ~/Downloads/rdmotors.db
exit
cd home/user
cd ~ find . -name "rdmotors.db"
cd ~
find . -name "rdmotors.db"
sqlite3 rdmotors.db
find / -name '*.db' 2>/dev/null
find / -name '*rdmotors.db' 2>/dev/null
ls -lh /app/database/rdmotors.db /root/rdmotors.db /root/Downloads/rdmotors.db /root/database/rdmotors.db
sqlite3 /root/rdmotors.db
ls -lh /app/database/rdmotors.db /root/rdmotors.db /root/Downloads/rdmotors.db /root/database/rdmotors.db
sqlite3 /root/database/rdmotors.db
cp /root/rdmotors.db /app/database/rdmotors.db
ls -lh /app/database/rdmotors.db /root/rdmotors.db /root/Downloads/rdmotors.db /root/database/rdmotors.db
sqlite3 /root/database/rdmotors.db
sqlite3 /root/rdmotors.db
docker exec -it rdmotors-bot bash
docker cp rdmotors-bot:/app/database/rdmotors.db /root/rdmotors.db
sqlite3 /root/rdmotors.db
docker cp rdmotors-bot:/app/database/rdmotors.db /root/rdmotors.db
sqlite3 /root/rdmotors.db
docker inspect rdmotors-bot
ls ./database/rdmotors.db
docker-compose up -d
docker exec -it rdmotors_bot /bin/bash
docker ps
docker ps -a
docker exec -it rdmotors-bot /bin/bash
docker volume ls
ls ./database/rdmotors.db
sqlite3 ./database/rdmotors.db
docker cp rdmotors-bot:/app/database/rdmotors.db /path/on/host/rdmotors.db
docker cp rdmotors-bot:/app/database/rdmotors.db /home/user/rdmotors.db
docker cp rdmotors-bot:/app/database/rdmotors.db /Users/user/rdmotors.db
docker cp rdmotors-bot:/app/database/rdmotors.db /Users/defacto092/rdmotors.db
docker cp rdmotors-bot:/app/database/rdmotors.db /Users/defacto092/rdmotors.dbDC
docker cp rdmotors-bot:/app/database/rdmotors.db /Users/defacto092/rdmotors.db
sqlite3 /app/database/rdmotors.db
docker logs rdmotors-bot
docker exec -it rdmotors-bot /bin/bash
docker cp rdmotors-bot:/app/database/rdmotors.db /home/user/rdmotors.db
docker cp rdmotors-bot:/app/database/rdmotors.db /Users/defacto092/rdmotors.db
docker cp rdmotors-bot:/app/database/rdmotors.db /Users/defacto092/Downloads
docker cp rdmotors-bot:/app/database/rdmotors.db /Users/defacto092/Downloads/
ls /Users/defacto092/Downloads/
docker cp rdmotors-bot:/app/database/rdmotors.db /Users/defacto092/Downloads/rdmotors.db
docker cp rdmotors-bot:/app/database/rdmotors.db /Users/defacto092
docker exec -it rdmotors-bot /bin/bash
docker cp rdmotors-bot:/app/database/rdmotors.db ~/Desktop/rdmotors.db
docker cp rdmotors-bot:/app/database/rdmotors.db Users/defacto092/Desktop/rdmotors.db
docker restart rdmotors-bot
docker cp rdmotors-bot:/app/database/rdmotors.db Users/defacto092/Desktop/rdmotors.db
docker cp rdmotors-bot:/app/database/rdmotors.db /Users/defacto092/Downloads/rdmotors.db
docker exec -it rdmotors-bot /bin/bash
docker exec -it rdmotors-bot /bin/bas
docker cp rdmotors-bot:/app/database/rdmotors.db /Users/defacto092/rdmotors.db
docker exec -it rdmotors-bot /bin/bash
docker cp rdmotors-bot:/app/database.rdmotors.db Users/defacto092/Downloads/rdmotors.db
docker cp rdmotors-bot:/app/database.rdmotors.db /Users/defacto092/Downloads/rdmotors.db
scp root@193.169.188.220:/root/rdmotors.db /Users/defacto092/Downloads
docker cp rdmotors-bot:/app/database/rdmotors.db ~/Downloads/
docker exec -it rdmotors-bot /bin/bash
docker cp rdmotors-bot:/app/database/rdmotors.db /root/rdmotors.db
scp root@193.169.188.220/app/database/rdmotors.db /Users/defacto092/Downloads
docker exec -it rdmotors-bot /bin/bash
docker cp /root/rdmotors.db rdmotors-bot:/app/database/rdmotors.db
docker cp /root/rdmotors.db rdmotors-ʼbot:/app/database/rdmotors.db
ls -la /root/rdmotors.db
docker logs -f rdmotors-bot
ls -l /app/database/rdmotors.db
docker restart rdmotors-bot
docker logs -f rdmotors-bot
docker exec -it rdmotors-bot
docker exec -it rdmotors-bot /bin/bash/
docker exec -it rdmotors-bot /bin/bash
docker cp /root/rdmotors.db rdmotors-bot:/app/database/rdmotors.db
ls -la /app/database/rdmotors.db
docker restart rdmotors-bot
ls -la /app/database/rdmotors.db
ls -la /root/rdmotors.db
docker logs rdmotors-bot
docker logs -а rdmotors-bot
docker logs -f rdmotors-bot
docker ps
docker e7e0c4b36117:/app/database/rdmotors.dbdocker cp e7e0c4b36117:/app/database/rdmotors.db /Users/defacto092/Downloads/rdmotors.db
docker cp e7e0c4b36117:/app/database/rdmotors.db /Users/defacto092/Downloads/rdmotors.db
ls -l /app/database/rdmotors.db
chmod 666 /app/database/rdmotors.db
ls -l /app/database/rdmotors.db
docker logs -f rdmotors-bot
docker exec -it rdmotors-bot /bin/bash
docker cp e7e0c4b36117:/app/database/rdmotors.db /Users/defacto092/Downloads/rdmotors.dbdocker cp e7e0c4b36117:/app/database/rdmotors.db /root/rdmotors.db
docker cp e7e0c4b36117:/app/database/rdmotors.db /root/rdmotors.db
docker logs -f rdmotors-bot
docker cp /root/rdmotors.db e7e0c4b36117:/app/database/rdmotors.db
docker logs -f rdmotors-bot
docker cp /root/rdmotors.db e7e0c4b36117:/app/database/rdmotors.db
docker cp e7e0c4b36117:/app/database/rdmotors.db /Users/defacto092/Downloads/rdmotors.db
docker cp e7e0c4b36117:/app/database/rdmotors.db /Users/defacto092/Downloads/rdmotors.dbdocker cp e7e0c4b36117:/app/database/rdmotors.db /root/rdmotors.db
docker cp e7e0c4b36117:/app/database/rdmotors.db /Users/defacto092/Downloads/rdmotors.db
docker cp /root/rdmotors.db e7e0c4b36117:/app/database/rdmotors.db
docker cp /root/rdmotors.db
docker cp e7e0c4b36117:/app/database/rdmotors.db /root/rdmotors.db
sqlite3 /app/database/rdmotors.db
sqlite3 /root/rdmotors.db
docker logs -f  % scp root@193.169.188.220:/root/rdmotors.db /Users/defacto092/Downloads/rdmotors.d
docker ps
docker logs -f e7e0c4b36117
ls -l /app/database/rdmotors.db
chmod 666 /app/database/rdmotors.db
ls -l /app/database/rdmotors.db
docker restart rdmotors-bot
docker logs -f e7e0c4b36117
sqlite3 /root/rdmotors.db
ls -l /app/database/rdmotors.db
lsof /app/database/rdmotors.db
docker ps
docker logs -f e7e0c4b36117
sqlite3 /root/rdmotors.db
docker cp e7e0c4b36117:/app/database/rdmotors.db /root/rdmotors.db
docker cp rdmotors-bot:/app/database/rdmotors.db /root/rdmotors.db
docker cp e7e0c4b36117:/app/database/rdmotors.db /root/rdmotors.db
sqlite3 /root/rdmotors.db
docker cp e7e0c4b36117:/app/database/rdmotors.db /root/rdmotors.db
sqlite3 /root/rdmotors.db
docker cp e7e0c4b36117:/app/database/rdmotors.db /root/rdmotors.db
sqlite3 /root/rdmotors.db
docker cp e7e0c4b36117:/app/database/rdmotors.db /root/rdmotors.db
sqlite3 /root/rdmotors.db
sudo apt update
sudo apt install mysql-server
sudo mysql_secure_installation
mysql -u root -p
sudo apt install mysql-server
sudo systemctl status mysql
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
sudo systemctl restart mysql
systemctl status mysql.service
journalctl -xeu mysql.service
sudo mysqld --help --verbose
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
sudo systemctl restart mysql
sudo mysql -u root -p
sudo ufw allow 3306
sudo ufw status
sudo ufw enable
sudo ufw allow 3306
sudo ufw status
sudo systemctl restart mysql
systemctl status mysql
sudo ufw status
mysql -u defacto092 -p -h 193.169.188.220
git pull origin main
sudo nano /etc/systemd/system/rdmotors-bot.service
/Users/defacto092/PycharmProjects
docker build -t my-telegram-bot .
docker run --env-file .env my-telegram-bot
docker-compose up -d --build
find ~ -name "docker-compose.yml"
docker ps
git --version
cd /Users/defacto092/PycharmProjects
git clone https://github.com/defacto09/rdmotors.git
git pull origin main
docker-compose down  # Зупиняє контейнер
docker-compose up -d --build  # Перезапускає з новими змінами
docker-compose --version
sudo usermod -aG docker $USER
sudo curl -L "https://github.com/docker/compose/releases/download/$(curl -s https://api.github.com/repos/docker/compose/releases/latest | jq -r .tag_name)/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version
cd rdmotors
ls
docker-compose up -d --build
nano .env
docker-compose up -d --build
docker ps
docker logs rdmotors_bot
git pull
docker-compose up -d --build
docker ps
docker-compose up -d --build
pip show mysql-connector-python
docker-compose up -d --build
nano docker-compose.yml
docker-compose up -d --build
docker images
docker rmi 01a274992ef0 9aa727bcc6b2
docker rmi 01a274992ef0 9aa727bcc6b2іе
docker stop 01a274992ef0 9aa727bcc6b2іе
docker images
docker-compose up --build
docker --version
docker-compose --version
docker-compose down
docker-compose pull
docker-compose up
docker ps -a
docker images
# Remove dangling images (those tagged <none>)
docker image prune -f
# Remove stopped containers
docker container prune -f
# Remove all related images
docker rmi rdmotors_telegram-bot defacto092/rdmotors-bot:v1.0
# Pull fresh base image
docker pull defacto092/rdmotors-bot:v1.0
# Then rebuild
docker-compose build --no-cache
docker-compose up
# Stop and remove all containers (forcefully if needed)
docker-compose down --rmi all --remove-orphans
# Remove all containers (including running ones)
docker rm -f $(docker ps -aq)
# Remove all images
docker rmi -f $(docker images -aq)
# Clean up system
docker system prune -a -f --volumes
# Remove old version
sudo apt remove docker-compose
# Install new version (as plugin)
sudo apt update
sudo apt install docker-compose-plugin
# Verify installation
docker compose version
# Pull fresh base image
docker pull defacto092/rdmotors-bot:v1.0
# Rebuild with new Docker Compose
docker compose build --no-cache
docker compose up
# Install new version (as plugin)
dokcer ps
docker ps
docker compose up
docker ps
docker ps -a
docker images
docker run -d --name rdmotors-bot defacto092/rdmotors-bot:v1.0
sqlite3 /app/database/rdmotors.db
docker logs rdmotors-bot
# Clean up system
docker cp e7e0c4b36117:/app/database/rdmotors.db /root/rdmotors.db
docker ps
docker cp e57c05977524:/app/database/rdmotors.db /root/rdmotors.db
ping 193.169.188.220
ssh root@193.169.188.220
sqlite3 /root/rdmotors.db
sqlite3 /app/database/rdmotors.db
find / -type f -name "rdmotors.db" 2>/dev/null
docker cp rdmotors-bot:/app/database/rdmotors.db /root/rdmotors.db
docker ps
docker cp e57c05977524:/app/database/rdmotors.db /root/rdmotors.db
sqlite3 /root/rdmotors.db
docker cp e57c05977524:/app/database/rdmotors.db /root/rdmotors.db
sqlite3 /root/rdmotors.db
docker cp e57c05977524:/app/database/rdmotors.db /root/rdmotors.dbsudo systemctl status ssh
sudo systemctl status ssh
sudo service ssh status
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
sudo nano /etc/my.cnf
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
sudo systemctl restart mysql
scp root@193.169.188.220:/root/rdmotors.db ~/Downloads/
scp root@193.169.188.220:/root/rdmotors.db /Users/defacto092/PycharmProjects/PythonProject1
scp root@193.169.188.220:/root/rdmotors.db ~/Downloads/scp root@193.169.188.220:/root/rdmotors.db .
scp root@193.169.188.220:/root/rdmotors.db .
pwd
scp root@193.169.188.220:/root/rdmotors.db ~/Desktop/
chmod 600 /root/rdmotors.db  # Власник може читати/записувати
ls -la /root/rdmotors.db
chmod 711 /root  # Дозволити доступ до папки /root
tmux new-session -s rdmbot
docker ps
docker logs -f e7e0c4b36117
docker ps
docker docker exec -it e7e0c4b36117 sqlite3 /app/database/rdmotors.db "SELECT * FROM messages;"
docker exec -it e7e0c4b36117 sqlite3 /app/database/rdmotors.db "SELECT * FROM messages;"
docker exec -it e7e0c4b36117 bash
sudo systemctl status ssh
docker ps
docker images
docker run docker run -d --name rdmotors-bot defacto092/rdmotors-bot:v1.0
docker run -d --name rdmotors-bot defacto092/rdmotors-bot:v1.0
docker ps
sqlite3 /app/database/rdmotors.db
sqlite3 root/rdmotors.db
docker images
docker run -d --name rdmotors-bot rdmotors-telegram-bot
docker stop e57c05977524
docker rm e57c05977524
docker run -d --name rdmotors-bot rdmotors-telegram-bot
docker ps
docker ps -a
docker logs rdmotors-bot
docker run -d --name rdmotors-bot rdmotors-telegram-bot
docker stop e57c05977524
docker stop 37755df362ff
docker rm 37755df362ff
docker run -d --name rdmotors-bot rdmotors-telegram-bot
docker logs rdmotors-bot
docker stop rdmotors-bot
docker rm rdmotors-bot
docker build -t rdmotors-telegram-bot .
cd /root/rdmotors-bot
docker build -t rdmotors-telegram-bot .
docker run -d --name rdmotors-bot rdmotors-telegram-bot
docker ps
git remote add origin https://github.com/defacto09/rdmotors.git
git push -u origin master
pwd
git remote add origin https://github.com/defacto09/rdmotors.git
git init
git remote add origin https://github.com/defacto09/rdmotors.git
git add .
git clone https://github.com/defacto09/rdmotors.git
rm -rf rdmotors
git clone https://github.com/defacto09/rdmotors.git
docker build -t rdmotors-telegram-bot .
cd /root/rdmotors/
docker build -t rdmotors-telegram-bot .
docker ps
docker images
docker build -t rdmotors-telegram-bot .
curl https://registry-1.docker.io/v2/
docker build --no-cache -t rdmotors-telegram-bot .
docker ps
docker images
docker run -t 5f865e6a7d26
docker login
docker tag rdmotors-telegram-bot yourusername/rdmotors-telegram-bot
docker push defacto092/rdmotors-telegram-bot
docker pull defacto092/rdmotors-telegram-bot
docker run -d --name rdmotors-bot yourusername/rdmotors-telegram-bot
docker run -d --name rdmotors-bot defacto092/rdmotors-telegram-bot
docker stop rdmotors-bot
docker rm rdmotors-bot
docker run -d --name rdmotors-bot-new defacto092/rdmotors-telegram-bot
docker images
docker pull defacto092/rdmotors-telegram-bot
docker load -i /root/rdmotors/rdmotors-telegram-bot.tar
sudo iptables -L
docker images
docker run -rm rdmotors-telegram-bot
docker run -t rdmotors-telegram-bot
docker load -i /root/rdmotors/rdmotors-telegram-bot.tar
docker run -d --name rdmotors-bot rdmotors-telegram-bot:latest
docker ps
sqlite3 /app/database/rdmotors
sqlite3 /app/database/rdmotors.db
find / -type f -name "*.db"
sqlite3 /root/rdmotors.db
find / -type f -name "*.db"
sqlite3 /root/database/rdmotors.db
docker stop 7f8a908dcbdf
docker ps
docker ps -a
docker stop $(docker ps -aq)
sqlite3 /root/rdmotors.db
find / -type f -name "*.db"
find / -type f -name "*rdmotors.db"
sqlite3 /root/database/rdmotors.db
sqlite3 /app/database/rdmotors.db
sqlite3 /Users/defacto092/rdmotors.db
find / -type f -name "*.db" -exec du -h {} \;
find / -type f -name "*rdmotors.db" -exec du -h {} \;
sqlite3 /Users/defacto092/Downloads/rdmotors.db
sqlite3 /root/database/rdmotors.db
sqlite3 /root//rdmotors.db
find / -type f -name "*rdmotors.db" -exec du -h {} \;
docker ps
docker exec -it 7f8a908dcbdf bash
docker ps
docker stop 7f8a908dcbdf
docker ps
usermod -aG docker $USER
docker stop 7f8a908dcbdf
sudo docker stop 7f8a908dcbdf
sudo docker rm -f 7f8a908dcbdf
sudo systemctl status docker
nsenter --target 939 --mount --uts --ipc --net --pid
sudo docker rm -f 7f8a908dcbdf
docker ps
docker stop rdmotors-telegram-bot:latest
docker stop rdmotors-bot
sudo docker stop rdmotors-bot
sudo docker stop rdmotors-botsudo docker kill rdmotors-
sudo docker kill rdmotors-bot
sudo ps aux | grep docker
sudo systemctl restart docker
sudo snap restart docker
sudo snap run docker.kill rdmotors-bot
sudo /snap/docker/current/bin/docker kill rdmotors-bot
docker ps
docker ps -a
docker rm -f rdmotors-bot
docker ps -a
docker stop $(docker ps -aq) && docker rm $(docker ps -aq)
docker ps
docker images
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
docker images
docker stop $(docker ps -aq)
docker rmi $(docker images -aq)
docker ps -a
ps aux | grep python
sudo systemctl restart docker
docker ps
docker images
docker ps -a
ps aux | grep python
kill -9 4968
docker load -i /root/rdmotors/rdmotors-bot.tar
docker run -d --name rdmotors-bot -p 8000:8000 rdmotors-telegram-bot:latest
sqlite3 /root/rdmotors/rdmotors.db
sqlite3 /app/database/rdmotors.db
sqlite3 //database/rdmotors.db
find / -name rdmotors.db 2>/dev/null
sqlite3 /root/database/rdmotors.db
sqlite3 /root/database/rdmotors.db/
sqlite3 /root/rdmotors.db
docker exec -it rdmotors
docker exec -it rdmotors_bot
docker ps
docker exec -it rdmotorr-bot
docker exec -it rdmotors-bot
docker exec -it aba900a06872
docker exec -it aba900a06872 bin/bash
docker exec -it aba900a06872 bin/sh
docker exec -it aba900a06872 /bin/ash
docker exec -it aba900a06872 python
cd rdmotors
cd /rdmotors/app/
cd /root/rdmotors/app/
docker exec -it aba900a06872 
docker ps
find / -name "rdmotors.db" 2>/dev/null
/app/database/rdmotors.db
cd /app/database/rdmotors.db
cd /app/database/
docker ps
sqlite3 /app/database/rdmotors.db
docker ps
docker exec -it aba900a06872
docker exec -it aba900a06872 bash
docker ps
docker cp aba900a06872:/app/database/rdmotors.db /root/rdmotors.db
docker exec -it aba900a06872 bash
docker cp aba900a06872:/app/database/rdmotors.db /root/rdmotors.db
docker exec -it aba900a06872 bash
docker cp aba900a06872:/app/database/rdmotors.db /root/rdmotors.db
docker ps
docker logs -f aba900a06872
docker exec -it aba900a06872 bash
docker ps
docker ps
docker stop aba900a06872
sudo docker stop aba900a06872
ls -l /var/run/docker.sock
sudo usermod -aG docker $USER
sudo docker rm -f aba900a06872
sudo journalctl -u docker.service
ls -l /run/docker.sock
cat /lib/systemd/system/docker.service
sudo nano /lib/systemd/system/docker.service
docker rm $(docker ps -aq)
docker stop $(docker ps -q)       # Зупинити всі запущені контейнери
docker rm $(docker ps -aq)        # Видалити всі контейнери (зупинені та неактивні)
docker stop $(docker ps -q)       # Зупинити всі запущені контейнери
docker rm $(docker ps -aq)        # Видалити всі контейнери (зупинені та неактивні)
sudo chown root:docker /var/run/docker.sock
sudo chmod 660 /var/run/docker.sock
sudo systemctl stop docker
sudo dockerd -H unix:///var/run/docker.sock
sudo -i
docker ps
systemctl status docker
systemctl start docker
systemctl status docker
ede
docker ps
ls -l /var/run/docker.sock
systemctl restart docker
journalctl -u docker.service -n 50 --no-pager
df -h
ls -ld /var/run
dockerd --debug
aa-status
ls -ld /var/run
systemctl stop docker
rm -rf /var/run/docker.sock
rm -rf /var/lib/docker/network/files/*
systemctl start docker
systemctl status docker
ls -l /var/run/docker.sock
ls -l /run/docker.sock
ps aux | grep dockerd
snap stop docker
еіещзkill 16465
kill 16465
snap remove docker
systemctl restart docker
systemctl status docker
