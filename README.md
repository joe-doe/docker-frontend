# tradeline

Assignment for developer position.

## Setup Docker API (from [here](https://stackoverflow.com/questions/37178824/how-do-i-find-the-docker-rest-api-url))

Here is how you enabled it on Ubuntu 16.04 (Xenial Xerus).

Edit the docker service file (it is better to avoid directly editing /lib/systemd/system/docker.service as it will be replaced on upgrades)

```bash
sudo systemctl edit docker.service
```

Add the following content

```bash
[Service]
ExecStart=
ExecStart=/usr/bin/docker daemon -H fd:// -H tcp://0.0.0.0:2100
```

For docker 18+, the content is a bit different:
```bash

[Service]
ExecStart=
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
