# Import socket module
import socket
import numpy as np
from egcd import egcd

alphabet = "abcdefghijklmnopqrstuvwxyz "
letter_to_index = dict(zip(alphabet, range(len(alphabet))))
index_to_letter = dict(zip(range(len(alphabet)), alphabet))


def matrix_mod_inv(matrix, modulus):
    """We find the matrix modulus inverse by
    Step 1) Find determinant
    Step 2) Find determinant value in a specific modulus (usually length of alphabet)
    Step 3) Take that det_inv times the det*inverted matrix (this will then be the adjoint) in mod 26
    """

    det = int(np.round(np.linalg.det(matrix)))  # Step 1)
    det_inv = egcd(det, modulus)[1] % modulus  # Step 2)
    matrix_modulus_inv = (
        det_inv * np.round(det * np.linalg.inv(matrix)).astype(int) % modulus
    )  # Step 3)

    return matrix_modulus_inv


def encrypt(message, K):
    encrypted = ""
    message_in_numbers = []

    for letter in message:
        message_in_numbers.append(letter_to_index[letter])

    split_P = [
        message_in_numbers[i: i + int(K.shape[0])]
        for i in range(0, len(message_in_numbers), int(K.shape[0]))
    ]

    for P in split_P:
        P = np.transpose(np.asarray(P))[:, np.newaxis]

        while P.shape[0] != K.shape[0]:
            P = np.append(P, letter_to_index[" "])[:, np.newaxis]

        numbers = np.dot(K, P) % len(alphabet)
        n = numbers.shape[0]

        for idx in range(n):
            number = int(numbers[idx, 0])
            encrypted += index_to_letter[number]

    return encrypted


# Create a socket object
s = socket.socket()

# Define the port on which you want to listen
port = 12345

# Bind the socket to the port
s.bind(('', port))
print("Socket binded to %s" % (port))

# Put the socket into listening mode
s.listen(5)
print("Socket is listening")

# Accept a connection from client
c, addr = s.accept()
print('Got connection from', addr)

message = "lokeshchowdhary"
K = np.matrix([[3, 3, 4], [2, 5, 8], [4, 6, 9]])
Kinv = matrix_mod_inv(K, len(alphabet))

encrypted_message = encrypt(message, K)

c.send(encrypted_message.encode())
c.send(Kinv.tobytes())

# Close the connection

