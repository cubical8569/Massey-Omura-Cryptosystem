from message import Message
import random
import sympy

class User:
    def __init__(self, cryptosystem, id):
        self.cryptosystem = cryptosystem

        if id not in cryptosystem.users:
            self.id = id
            cryptosystem.users[id] = self
        else:
            raise KeyError("User with this name already exists")

        self.e = random.randrange(3, self.cryptosystem.curve.n) * self.cryptosystem.curve.h + 1
        # генерируем нечётное число в промежутке (3, n * 2) => (e, n * 2) = 1
        self.d = sympy.mod_inverse(self.e, self.cryptosystem.curve.curve_points)

    def send_text(self, receiver_name, message_text):
        send_text = self.id + ": " + message_text

        for c in send_text:
            decrypted_elem = self.cryptosystem.encrypt_char(c)
            encrypted_elem = decrypted_elem * self.e

            m = Message(
                type=Message.Type.FIRST,
                sender_name=self.id,
                elem=encrypted_elem
            )

            self.cryptosystem.send(receiver_name=receiver_name, message=m)

    def receive_message(self, message):
        received_elem = message.elem

        if message.type == Message.Type.FIRST:
            answer_message = Message(
                type=Message.Type.SECOND,
                sender_name=self.id,
                elem=received_elem * self.e
            )

            self.cryptosystem.send(message.sender_name, answer_message)

        elif message.type == Message.Type.SECOND:
            answer_message = Message(
                type=Message.Type.THIRD,
                sender_name=self.id,
                elem=received_elem * self.d
            )

            self.cryptosystem.send(message.sender_name, answer_message)

        else:
            clear_elem = received_elem * self.d
            received_text = self.cryptosystem.decrypt_char(clear_elem)

            print(received_text, end='')