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



'''
Connection for data validator microservice
'''
# Set up request socket
validator_socket = context.socket(zmq.REQ)
# Connect to remote socket
validator_socket.connect("tcp://localhost:5559")



'''
Connection for data validator microservice
'''
# Set up request socket
database_socket = context.socket(zmq.REQ)
# Connect to remote socket
database_socket.connect("tcp://localhost:4325")