import socket
import os, os.path
import sys
 
print("Connecting...")
if os.path.exists( "/tmp/python_unix_sockets_example" ):
  client = socket.socket( socket.AF_UNIX, socket.SOCK_DGRAM )
  client.connect( "/tmp/python_unix_sockets_example" )
  print("Ready.")
  print("Ctrl-C to quit.")
  print("Sending 'DONE' shuts down the server and quits.")
#  while True:
  try:
    #x = raw_input( "> " )
    x = sys.argv[1]
    if "" != x:
      print("SEND:", x)
      client.send( x )
  except KeyboardInterrupt, k:
    print("Shutting down.")
  client.close()
else:
  print("Couldn't Connect!")
print("Done")
