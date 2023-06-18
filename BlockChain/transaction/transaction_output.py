import json

class TransactionOutput:
    def __init__(self, public_key_hash: str, amount: int):
        self.public_key_hash = public_key_hash
        self.amount = amount

    def to_json(self) -> str:
        json_result = json.dumps({'amount': self.amount, 
                                  'public_key_hash': self.public_key_hash})
        return json_result