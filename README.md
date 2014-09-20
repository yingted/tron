# tron
Tron game server, client, and library for Python and Turing.
## Rules
Each iteration lasts at most 0.1 s (by default) and the initial position is a 50x49 board with the two light cycles pointed at each other. Because of the timeout, it makes sense to disable drawing the game unless you're debugging.
## Server requirements
You need `twisted`, `python`, and a web server with autoindex, such as Apache, `nginx` or even `python -mSimpleHTTPServer`.
## Usage
Run `./tron.py` and navigate to `./viewer.html`
## Packaging for Windows or Turing
Run `make tron-win32.zip` to package `twisted` and `zope` for Windows users.
## Bots
### Included
#### Turing
`tron_sample.t` uses the module in `tron.tu` and implements a greedy algorithm.
#### Python
`tron_sample.py` uses the module in `tron.py` and implements the same greedy algorithm as `tron_sample.t`.
#### User-controlled
`tron_tester.py` accepts keyboard input for the bot.
#### Strong bots
`voronoi.py` and `negamax.py` are examples of stronger bots. Compiled and optimized binaries are included.
They're based off of: http://www.a1k0n.net/2010/03/04/google-ai-postmortem.html
### Custom
You can import `tron.tu` or `tron.py` and make your own bot. You need a bot name and unique key (for tracking wins and losses). Encryption is not supported. See `tron_sample.*` for examples.
