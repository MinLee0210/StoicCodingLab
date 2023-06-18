import binascii
import copy
import json 

from block.block import Block
from block.utils import calculate_hash
from node.script import StackScript

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15

class Node:
    def __init__(self, blockchain: Block):
        self.blockchain = blockchain

    @staticmethod
    def validate_signature(public_key: bytes, signature: bytes, transaction_data: bytes):
        public_key_object = RSA.import_key(public_key)
        transaction_hash = SHA256.new(transaction_data)
        pkcs1_15.new(public_key_object).verify(transaction_hash, signature)

    def validate_funds(self, sender_address: bytes, amount: int) -> bool:
        sender_balance = 0
        current_block = self.blockchain
        while current_block: 
            if current_block.transaction_data['sender'] == sender_address:
                sender_balance = sender_balance - current_block.transaction_data['amount']
            if current_block.transaction_data['receiver'] == sender_address:
                sender_balance = sender_balance + current_block.transaction_data['amount']
            current_block = current_block.previous_block
        if amount <= sender_balance:
            return True
        else:
            return False
    
class NodeTransaction:
    def __init__(self):
        pass

    # def validate(self):
    #     self.validate_signature()
    #     self.validate_funds_are_owned_by_sender()
    #     self.validate_funds()

    def validate(self):
        for tx_input in self.inputs:
            input_dict = json.loads(tx_input)
            locking_script = self.get_locking_script_from_utxo(input_dict["transaction_hash"], input_dict["output_index"])
            self.execute_script(input_dict["unlocking_script"], locking_script)
            
    def get_locking_script_from_utxo(self, utxo_hash: str, utxo_index: int):
        transaction_data = self.get_transaction_from_utxo(utxo_hash)
        return json.loads(transaction_data["outputs"][utxo_index])["locking_script"]
    
    def validate_signature(self):
        transaction_data = copy.deepcopy(self.transaction_data)
        for count, tx_input in enumerate(transaction_data['inputs']):
            tx_input_dict = json.loads(tx_input)
            public_key = tx_input_dict.pop('public_key')
            signature = tx_input_dict.pop('signature')
            transaction_data['inputs'][count] = json.dumps(tx_input_dict)
            signature_decoded = binascii.unhexlify(signature.decode('utf-8'))
            public_key_bytes = public_key.encode('utf-8')
            public_key_object = RSA.import_key(binascii.unhexlify(public_key_bytes))
            transaction_bytes = json.dumps(transaction_data, indent=2).encode('utf-8')
            transaction_hash = SHA256.new(transaction_bytes)
            pkcs1_15.new(public_key_object).verify(transaction_hash, signature_decoded)

    def get_transaction_from_utxo(self, utxo_hash: str) -> dict:
        current_block = self.blockchain
        while current_block:
            if utxo_hash == current_block.transaction_hash:
                return current_block.transaction_data
            current_block = current_block.previous_block

    def validate_funds_are_owned_by_sender(self):
        for tx_input in self.inputs:
            input_dict = json.loads(tx_input)
            public_key = input_dict["public_key"]
            sender_public_key_hash = calculate_hash(calculate_hash(public_key, hash_function="sha256"), hash_function="ripemd160")
            transaction_data = self.get_transaction_from_utxo(input_dict["transaction_hash"])
            public_key_hash = json.loads(transaction_data["outputs"][input_dict["output_index"]])["public_key_hash"]
            assert public_key_hash == sender_public_key_hash

    def validate_funds(self):
        assert self.get_total_amount_in_inputs() == self.get_total_amount_in_outputs()

    def get_total_amount_in_inputs(self) -> int:
        total_in = 0
        for tx_input in self.inputs:
            input_dict = json.loads(tx_input)
            transaction_data = self.get_transaction_from_utxo(input_dict["transaction_hash"])
            utxo_amount = json.loads(transaction_data["outputs"][input_dict["output_index"]])["amount"]
            total_in = total_in + utxo_amount
        return total_in

    def get_total_amount_in_outputs(self) -> int:
        total_out = 0
        for tx_output in self.outputs:
            output_dict = json.loads(tx_output)
            amount = output_dict["amount"]
            total_out = total_out + amount
        return total_out
    
    def execute_script(self, unlocking_script, locking_script):
        unlocking_script_list = unlocking_script.split(" ")
        locking_script_list = locking_script.split(" ")
        stack_script = StackScript(self.transaction_data)
        for element in unlocking_script_list:
            if element.startswith("OP"):
                class_method = getattr(StackScript, element.lower())
                class_method(stack_script)
            else:
                stack_script.push(element)
        for element in locking_script_list:
            if element.startswith("OP"):
                class_method = getattr(StackScript, element.lower())
                class_method(stack_script)
            else:
                stack_script.push(element)