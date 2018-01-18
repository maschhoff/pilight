# pilight
pilight configuration and tools

# RecordReceiveCallback.py

a small pilight socket recorder for sending devices states to openhab2
 - requires pip3 install pilight
 - requires pip3 install requests

since the pilight binding for openhab only works well on openhab1 and I dont care about version 1 bindings I tryed to find out a way to make pilight communicate with openhab2. This is an approach using the openhab2 REST API.

with this socket reader you can read all pilight received devices filter them and send your device state to openhab2 API
you have to edit the supported protocols for your protocols and you have to edit the item list with your ideas.
And you have to edit the openhab2 API IP.
Everything will be logged to piRecReci.log

For sending commands from openhab2 to pilight see my openhab folder under scripts, I use the Exec binding and curl for connection to pilight 8+ API
