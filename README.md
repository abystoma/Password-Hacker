A bit intermediate example of hacking a json server, using brute force

The server sends and receives data in the json format, but requires an initial login (username) apart from the usual password

# Usage

1. Make sure you have python 3 installed
2. Run the server first, as thats the attack target using `python server.py`
3. Create another terminal and run the client code using `python hack_json.py`
4. The server should print the correct login and password combo and the client should come up with the same combo after retrying for some time

# TODO

1. Add metrics for time taken and failed combo count
2. Server generates username from logins.txt