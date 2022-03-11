Micropython-https-server
========================

This is some example code thrown together to demonstrate how to implement a
very simple https web server. I needed one for a project and could not get a
working example from one place. Instead I had to figure out the details from
a couple of examples, questions in forums and other sources of information.

So this is my example implementation. It's not a framework, but code you can
take and modify to fit your needs. The whole code is in `HTTPSServer.py`, it
requires a certificate and matching key file to run. Also included in this
repository is everything else to set things up, if your platform is an
[ESP32](https://en.wikipedia.org/wiki/ESP32) running
[Micropython](https://micropython.org/). If you have
[ampy](https://github.com/scientifichackers/ampy) installed, the included
shellscript `update.sh` should configure and upload everything required.
`main.py` includes some convenience functions and also sets up networking.
It should get autoloaded by Micropython upon startup. The https server needs
to be started up by hand though, to make sure you can get a foot in the door.
Remember: example, not framework.

The web server code includes support for delivering a favicon.ico (if the
file is found on the device), and a very lame implementation of authorization.
The http request header is nicely wrapped in a dictionary for easy access. But
this code does not include any kind of support for handling forms, neither for
GET nor for POST requests.

Python and myself will never become friends, so this code might not be
elegant, but at least it was working on my [ESP32 NodeMCU](https://www.berrybase.de/dev.-boards/esp8266-esp32-d1-mini/boards/esp32-nodemcu-development-board)
using Micropython 1.18 when I wrote it. It was only put here to save other
from the pain, I experienced trying to get this done. While I don't plan on
writing any updates to this code, pull requests will be processed.

Hope this helps you as it would have helped me, \
SvOlli

P.S.: [Python](https://en.wikipedia.org/wiki/Python_(programming_language))
is the [BASIC](https://en.wikipedia.org/wiki/BASIC) of the 21st century.
