# Doug's Valheim Server Utility


## Installation

Requires Python3.

```shell
git clone git@github.com/dougthor42/dougs-valheim-server.git
cd dougs-valheim-server
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

Create `secrets.yml` in the repository root.

```yaml
---
foo: 'enter the secret that doug gave you personally.'
```

As this point you should be good to go.


## Usage

(Note: the virtual environment made above must be active.)

First, check the current status of the server:

```
$ dougs_valheim_server status
The server is UP with an IP address of: 33.99.24.590

$ dougs_valheim_server stop
Stopping server...
Stopped

$ dougs_valheim_server status
The server is DOWN. Run `dougs_valheim_server start` to start it.

$ dougs_valheim_server start
Starting server...
The server has been started. IP address: 94.123.57.999

$ dougs_valheim_server status
The server is UP with an IP address of: 94.123.57.999
```