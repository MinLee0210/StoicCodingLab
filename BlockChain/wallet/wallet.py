import json
import base58
import binascii

from utils import calculate_hash, generate_transaction_data, convert_transaction_data_to_bytes
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15

from transaction.transaction_input import TransactionInput
from transaction.transaction_output import TransactionOutput

class Owner:
    def __init__(self, private_key: RSA.RsaKey, public_key:bytes, bitcoin_address:bytes):
        self.private_key = private_key
        self.public_key = public_key
        self.bitcoin_address = bitcoin_address


def initialize_wallet():
    private_key = RSA.generate(2048)
    public_key = key.publickey().export_key()
    hash_1 = calculate_hash(public_key, hash_function='sha256')
    hash_2 = calculate_hash(hash_1, hash_function='ripemd160')
    bitcoin_address = base58.b58encode(hash_2)
    return Owner(private_key, public_key,bitcoin_address)

# class Transaction:
#     def __init__(self, owner: Owner, 
#                  receiver_bitcoin_address: bytes, 
#                  amount: int,
#                  signature: str=''):
#         self.owner = owner
#         self.receiver_bitcoin_address = receiver_bitcoin_address
#         self.amount = amount
#         self.signature = signature

#     def generate_data(self) -> bytes:
#         transaction_data = generate_transaction_data(self.owner.bitcoin_address,
#                                                      self.receiver_bitcoin_address,
#                                                      self.amount)
#         converted_result = convert_transaction_data_to_bytes(transaction_data)
#         return converted_result
    
#     def sign(self) -> str:
#         transaction_data = self.generate_data()
#         hash_object = SHA256.new(transaction_data)
#         signature = pkcs1_15.new(self.owner.private_key).sign(hash_object)
#         signature = binascii.hexlify(signature).decode('utf-8')
#         return signature
    
#     def send_to_nodes(self):
#         message = {
#             'sender_address': self.owner.bitcoin_address, 
#             'receiver_address': self.receiver_bitcoin_address, 
#             'amount': self.amount, 
#             'signature': self.signature
#         }
#         return message

class Transaction:
    def __init__(self, owner: Owner, 
                 inputs: list[TransactionInput], 
                 outputs: list[TransactionOutput]):
        self.owner = owner
        self.inputs = inputs
        self.outputs = outputs

    def sign_transaction_data(self):
        transaction_dict = {
            "inputs": [tx_input.to_json(with_signature_and_public_key=False) for tx_input in self.inputs],
            "outputs": [tx_output.to_json() for tx_output in self.outputs]
        }
        transaction_bytes = json.dumps(transaction_dict, indent=2).encode('utf-8')
        hash_object = SHA256.new(transaction_bytes)
        signature = pkcs1_15.new(self.owner.private_key).sign(hash_object)
        return signature

    def sign(self):
        signature_hex = binascii.hexlify(self.sign_transaction_data()).decode("utf-8")
        for transaction_input in self.inputs:
            transaction_input.signature = signature_hex
            transaction_input.public_key = self.owner.public_key_hex

    def send_to_nodes(self):
        return {
            "inputs": [i.to_json() for i in self.inputs],
            "outputs": [i.to_json() for i in self.outputs]
        }