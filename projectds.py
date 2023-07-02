from mpi4py import MPI
import time

# Initialize MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Define tags for message types
TAG_MESSAGE = 1
TAG_RESPONSE = 2

if size < 2:
    print("This program requires at least 2 processors.")
    exit()

# Initialize Lamport timestamp for each process
lamport_timestamp = 0

if rank == 0:
    while True:
        # Take user input
        message = input("Enter a message (or 'exit' to quit): ")

        if message == 'exit':
            break

        # Update Lamport timestamp
        lamport_timestamp += 1

        # Get current Lamport timestamp
        timestamp = lamport_timestamp

        # Send message and timestamp to processor 1
        comm.send((message, timestamp), dest=1, tag=TAG_MESSAGE)
        comm.Barrier()

        # Receive response message and timestamp from processor 1
        response, response_timestamp = comm.recv(source=1, tag=TAG_RESPONSE)

        # Update Lamport timestamp
        lamport_timestamp = max(lamport_timestamp, response_timestamp) + 1

        # Display received response message and its timestamp
        print(f"Received response: {response} (Timestamp: {response_timestamp})")

        if response == 'exit':
            break

else:
    while True:
        # Receive message and timestamp from processor 0
        data = comm.recv(source=0, tag=TAG_MESSAGE)
        message, timestamp = data

        # Update Lamport timestamp
        lamport_timestamp = max(lamport_timestamp, timestamp) + 1

        # Display received message and timestamp
        print(f"Received message: {message} (Timestamp: {timestamp})")

        # Take user input for response message
        response = input("Enter a response message: ")

        # Update Lamport timestamp
        lamport_timestamp += 1

        # Send response message and timestamp to processor 0
        comm.send((response, lamport_timestamp), dest=0, tag=TAG_RESPONSE)

        if response == 'exit':
            break
