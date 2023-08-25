# socksifer
A reverse socks5 proxy that permits operators to proxy traffic through where ever the socksifer-client connected from. 

### Debugging Steps
Install socksifer
```
python3 -m venv env
. env/bin/activate
python3 -m pip install -r requirements.txt
```

Execute socksifer
```
(env) skyler@socksifer:~/socksifer$ python3 socksifer.py 
Welcome to the Socksifer CLI, type help or ? to get started
[*] Starting SocketIO Server on http://127.0.0.1:1337/
(socksifer)~#
```

Execute socksifer-client
```
(env) skyler@socksifer:~/socksifer$ python3 socksifer-client.py http://127.0.0.1:1337/

# You'll recieve a message similiar to the following on the Socksifer CLI
[+] aXLVbtMmGm is listening on 127.0.0.1:9066
```

Proxy traffic
```
xfreerdp /v:host /u:username /p:pasword /proxy:socks5://127.0.0.1:9066
```

Change debug
```
# Within the Socksifer CLI change the debug mode to two.
(socksifer)~# debug 2
[+] Set the debug level to 2
(socksifer)~#
```

Reproxy traffic
```
xfreerdp /v:host /u:username /p:pasword /proxy:socks5://127.0.0.1:9066
```
