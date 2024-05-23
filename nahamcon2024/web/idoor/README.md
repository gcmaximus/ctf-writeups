# iDoor
It's Apple's latest innovation, the "iDoor!" ... well, it is basically the Ring Doorbell camera, but the iDoor offers a web-based browser to monitor your camera, and super secure using ultimate cryptography with even SHA256 hashing algorithms to protect customers! Don't even think about snooping on other people's cameras!!

# Flag
flag{770a058a80a9bca0a87c3e2ebe1ee9b2}

# Solution
View other customer's cameras by SHA256-ing different integers and appending the hex digest to the base URL. See `req.py`