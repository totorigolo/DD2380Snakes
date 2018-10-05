
Prerequisites
---
* Java SDK > ~7
* Nodejs & NPM



Getting Started
---
* Follow installation instructions here to start the server: https://github.com/cygni/snakebot 
* Follow installation instructions here for the web-interface: https://github.com/cygni/snakebot-webclient


The web-interface is only necessary to start tournaments, you don't need it to begin with.


<br/>
<br/>

If all went well you can navigate in to the baselines folder and run 
```bash
> sh local.sh
```
To view the game using the UI you will have to have started the webclient.


Hosting Tournaments
---

1. Start the webclient 
2. Press Login & use the credentials; username: emil, password: lime
3. Press Tournament
4. Snakes can now join the game by joining a "tournament" from the clients 

For example from the python client you join a tournament by passing "-v tournament" to the main file. Just dig through
the source to find out how to join tournaments for every partiular client! :) 
