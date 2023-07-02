from mpi4py import MPI
import time

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Define the sender and receiver ranks
sender_rank = 0
receiver_rank = 1

if rank == sender_rank:
    # Sender process
    total_messages = 0
    total_time = 0
    timestamp = 1

    while True:
        # Get the message from the user
        message = input("Enter your message: ")

        # Start the timer
        start_time = time.time()

        # Send the message to the receiver with timestamp
        comm.send((message, timestamp), dest=receiver_rank)

        if message.lower() == "exit":
            break

        # Receive the response from the receiver
        response = comm.recv(source=receiver_rank)

        # Stop the timer
        end_time = time.time()
        elapsed_time = end_time - start_time

        # Print the response, sender timestamp, and timing information
        print("Response:", response)
        print("Sender Timestamp:", timestamp)
        print("Elapsed Time:", elapsed_time, "seconds")

        # Accumulate total messages and total time
        total_messages += 1
        total_time += elapsed_time

        # Update the local timestamp
        timestamp += 1

    # Calculate efficiency
    efficiency = total_time / total_messages if total_messages > 0 else 0

    print("Total Messages:", total_messages)
    print("Total Time:", total_time, "seconds")
    print("Efficiency:", efficiency, "seconds per message")

elif rank == receiver_rank:
    # Receiver process

    while True:
        # Receive the message from the sender
        message, sender_timestamp = comm.recv(source=sender_rank)

        # Print the received message and sender timestamp
        print("Received message:", message)
        print("Sender Timestamp:", sender_timestamp)

        if message.lower() == "exit":
            break

        # Send a response to the sender
        response = "I have received the message"
        comm.send(response, dest=sender_rank)
