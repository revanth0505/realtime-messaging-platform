# Import socket module
import socket
import numpy as np

alphabet = "abcdefghijklmnopqrstuvwxyz "
letter_to_index = dict(zip(alphabet, range(len(alphabet))))
index_to_letter = dict(zip(range(len(alphabet)), alphabet))


def decrypt(cipher, Kinv):
    decrypted = ""
    cipher_in_numbers = []

    for letter in cipher:
        cipher_in_numbers.append(letter_to_index[letter])

    split_C = [
        cipher_in_numbers[i: i + int(Kinv.shape[0])]
        for i in range(0, len(cipher_in_numbers), int(Kinv.shape[0]))
    ]

    for C in split_C:
        C = np.transpose(np.asarray(C))[:, np.newaxis]
        numbers = np.dot(Kinv, C) % len(alphabet)
        n = numbers.shape[0]

        for idx in range(n):
            number = int(numbers[idx, 0])
            decrypted += index_to_letter[number]

    return decrypted


# Create a socket object
s = socket.socket()

# Define the port on which you want to connect
port = 12345

# Connect to the server on local computer
s.connect(('127.0.0.1', port))

# Receive data from the server and decode it
received = s.recv(1024).decode()
Kinv_bytes = s.recv(1024)

# Calculate the required buffer size for Kinv
Kinv_size = 3 * 3 * 8  # 3x3 matrix of float64 elements

# Receive the remaining bytes of Kinv
while len(Kinv_bytes) < Kinv_size:
    Kinv_bytes += s.recv(1024)

# Convert Kinv_bytes to a NumPy array
Kinv = np.frombuffer(Kinv_bytes, dtype=np.float64)

# Reshape Kinv to a 3x3 matrix
Kinv = Kinv.reshape(3, 3)

decrypted_message = decrypt(received, Kinv)

print("Encrypted Message: ", received)
print("Decrypted Message: ", decrypted_message)

# Close the connecti
