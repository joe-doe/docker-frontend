# Setup Docker API (from [here](https://stackoverflow.com/questions/37178824/how-do-i-find-the-docker-rest-api-url))

Here is how you enabled it on Ubuntu 16.04 (Xenial Xerus).

Edit the docker service file (it is better to avoid directly editing /lib/systemd/system/docker.service as it will be replaced on upgrades)

```bash
sudo systemctl edit docker.service
```

Add the following content

```bash
[Service]
ExecStart=/usr/bin/docker daemon -H fd:// -H tcp://0.0.0.0:2100
```

For docker 18+, the content is a bit different:
```bash

[Service]
ExecStart=/usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock -H tcp://0.0.0.0:2100
```

Save the modified file. Here I used port 2100, but any free port can be used.

Make sure the Docker service notices the modified configuration:

```bash
systemctl daemon-reload
```

Restart the Docker service:

```bash
sudo service docker restart
```

Test
```bash
curl http://localhost:2100/version
```

See the result

```json
{"Platform":{"Name":"Docker Engine - Community"},"Components":[{"Name":"Engine","Version":"18.09.5","Details":{"ApiVersion":"1.39","Arch":"amd64","BuildTime":"2019-04-11T04:10:53.000000000+00:00","Experimental":"false","GitCommit":"e8ff056","GoVersion":"go1.10.8","KernelVersion":"4.15.0-48-generic","MinAPIVersion":"1.12","Os":"linux"}}],"Version":"18.09.5","ApiVersion":"1.39","MinAPIVersion":"1.12","GitCommit":"e8ff056","GoVersion":"go1.10.8","Os":"linux","Arch":"amd64","KernelVersion":"4.15.0-48-generic","BuildTime":"2019-04-11T04:10:53.000000000+00:00"}
```

# `EXPERIMENTAL` version

I tried to realtime feed logs from containers to mongodb and then use websockets to retrieve data.
Everything works fine except the fact that I realize that pymongo needs all application subprocesses created
before connecting to mongodb server otherwise you get a weird behaviour. 

In my case I use a subprocess to monitor for running containers, feed them to a list and start a new subprocess
for every new running container that constantly read for logs and write them in mongodb.

I left code commented out on purpose because I intend to continue my effort but I had to deliver something working.
So comments in code as `EXPERIMENTAL` fall in this case.

# Dependencies

## System

1. Python 3 (tested on python 3.7)
2. Mongodb `EXPERIMENTAL`

   Installation: https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/
   
## Python
No need to install manually; just follow installation instructions.

1. Click	7.0
2. Flask	1.0.2
3. Flask-SocketIO	3.3.2
4. Jinja2	2.10.1
5. MarkupSafe	1.1.1
6. Werkzeug	0.15.2
7. certifi	2019.3.9
8. chardet	3.0.4
9. docker	3.7.2
10. docker-pycreds	0.4.0
11. idna	2.8
12. itsdangerous	1.1.0
13. pip	19.0.3
14. pymongo	3.8.0
15. python-engineio	3.5.1
16. python-socketio	3.1.2
17. requests	2.21.0
18. setuptools	40.8.0
19. six	1.12.0
20. urllib3	1.24.3	
21. websocket-client	0.56.0	

## Client
No need to install anything. Although web browser needs internet connection to access them.
1. jQuery
2. socketio `EXPERIMENTAL`
3. bootstrap

# Installation
In order to install the application, follow the steps below

* Clone the application form github
```bash
git clone https://github.com/joe-doe/tradeline.git
```

* Change to application directory
```bash
cd tradeline
```

* Create a virtual environment and activate it
```bash
virtualenv -p python3 venv
source venv/bin/activate
```

* Install all python dependencies
```bash
pip3 install -r requirements.txt
```

* Run application (while in virtual environment)
```bash
python assignment.py
```

Now navigate to http://0.0.0.0:5000/index and enjoy !

# Nice to have

* PEP-8
* Docstrings
* Tests
* Configuration
* Easy deploy
