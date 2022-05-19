import socket

# url or ip adress
urlip = ""
# port number not a string
portn = ""

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((urlip, portn))

msg = s.recv(1024)
new_string = msg.decode()
print(new_string)


# what you would like to submit to the server
submit = ""

s.send(bytes(submit , "utf-8"))