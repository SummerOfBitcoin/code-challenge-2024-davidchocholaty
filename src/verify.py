def valid_transaction_syntax(json_transaction):
    required = ["version", "locktime", "vin", "vout"]

    for field in required:
        if field not in json_transaction:
            #print('Required field is missing')
            return False
        
    if not isinstance(json_transaction["version"], int):
        #print('Invalid data type')
        return False
        
    if not isinstance(json_transaction["locktime"], int):
        #print('Invalid data type')
        return False

    if not isinstance(json_transaction["vin"], list):
        #print('Invalid data type')
        return False
    
    if not isinstance(json_transaction["vout"], list):
        #print('Invalid data type')
        return False

    # Check inputs
    for input in json_transaction['vin']:
        if not isinstance(input, dict):
            #print('Invalid data type')
            return False

        if 'txid' not in input or 'vout' not in input:
            #print('Invalid data type')
            return False

    # Check outputs
    for output in json_transaction['vout']:
        if not isinstance(output, dict):
            #print('Invalid data type')
            return False

        if 'scriptpubkey' not in output or 'value' not in output:
            #print('Invalid data type')
            return False
        
    return True


def parse_der_signature_bytes(der_signature):
    # Parse the DER signature    
    r_length = der_signature[3]
    r = der_signature[4:4 + r_length]
    s_length_index = 4 + r_length + 1
    s_length = der_signature[s_length_index]
    s = der_signature[s_length_index + 1:s_length_index + 1 + s_length]
    hash_type = der_signature[-1]
    
    return r, s, hash_type


def parse_der_signature(der_signature_with_hash_type):
    # Remove the hash_type from the DER signature
    der_signature = der_signature_with_hash_type[:-2]
    
    # Parse the DER signature
    der_bytes = bytes.fromhex(der_signature)
    r_length = der_bytes[3]
    r = int.from_bytes(der_bytes[4:4 + r_length], 'big')
    s_length_index = 4 + r_length + 1
    s_length = der_bytes[s_length_index]
    s = int.from_bytes(der_bytes[s_length_index + 1:s_length_index + 1 + s_length], 'big')
    hash_type = der_bytes[-1]
    
    return r, s, hash_type