import hashlib
import requests
import time
import uuid

import sys


def valid_proof(last_proof, proof):
    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:6] == "000000"

def proof_of_work(last_proof):
    proof = 0
    while valid_proof(last_proof, proof) is False:
        proof += 1

    return proof

def fetch_last_proof():
    URL = 'http://localhost:5000/last_proof'
    response = requests.get(url = URL)
    data = response.json()
    return data['last_proof']

def mine_block(proof, unique_id):
    URL = 'http://localhost:5000/mine'
    request = {
        "proof": proof,
        "sender": unique_id
    } 
    response = requests.post(url = URL, json = request)
    return response.json()

def get_uuid():
    try:
        id_file = open('my_id.txt')
        unique_id = id_file.read()
        if unique_id:
            id_file.close()
            return unique_id
    except:
        id_file = open('my_id.txt', 'w')
        new_uuid = str(uuid.uuid1()).replace('-', '')
        id_file.write(new_uuid)
        id_file.close()
        return new_uuid        


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    coins_mined = 0
    unique_id = get_uuid()
    # Run forever until interrupted
    while True:
        last_proof = fetch_last_proof()
        print("Calculating proof")
        start_time = time.time()
        proof = proof_of_work(last_proof)
        end_time = time.time()
        time_elapsed = end_time - start_time
        print(f"Proof calculated in {time_elapsed} seconds.")
        response = mine_block(proof, unique_id)
        if response:
            if response["message"] == 'New Block Forged':
                coins_mined += 1
                print(response["message"])
                print(f'{coins_mined} coins mined.')
            else:
                print(response["message"])
        else:
            print("POST request failed.")
