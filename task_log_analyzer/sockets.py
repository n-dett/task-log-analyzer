import zmq

# Set up zeroMQ environment
context = zmq.Context()

'''
Connection for data cleaning microservice
'''
# Set up request socket
data_clean_socket = context.socket(zmq.REQ)
# Connect to remote socket
data_clean_socket.connect("tcp://localhost:4377")