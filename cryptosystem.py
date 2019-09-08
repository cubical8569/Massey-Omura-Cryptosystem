from elliptic_curve import ECurve
import random

class Cryptosystem:

    def _init_alphabet(self):
        self.char_to_elem = [None] * 128
        self.elem_to_char = dict()

        i = 0
        while i != 128:
            print(i)

            degree = random.randrange(1, self.curve.n // 1e42)
            elem = self.curve.g * degree

            if not elem in self.elem_to_char:
                self.char_to_elem[i] = elem
                self.elem_to_char[elem] = i

                i += 1

    def encrypt_char(self, char):
        return self.char_to_elem[ord(char)]

    def decrypt_char(self, elem):
        return chr(self.elem_to_char[elem])

    def __init__(self):
        self.curve = ECurve()
        self._init_alphabet()
        self.users = dict()

    def send(self, receiver_name, message):
        self.users[receiver_name].receive_message(message)
        pass



