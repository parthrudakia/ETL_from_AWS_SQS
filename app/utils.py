import hashlib

def mask_pii(data, key):
    """
    Masks PII using SHA-256.

    Params:
    data (dict): The dictionary containing the PII data.
    key (str): The key in the dictionary whose value needs to be masked.

    Returns:
    str: The SHA-256 hash of the PII data.
    """
    return hashlib.sha256(data[key].encode()).hexdigest()

def flatten_json(data):

    """
    Flatten the JSON data and mask PII fields.

    Params:
    data (dict): The JSON data as a dictionary to be flattened and masked.

    Returns:
    dict: A dictionary with the flattened and masked PII data.
    """
    
    return {
        'user_id': data['user_id'],
        'device_type': data['device_type'],
        'masked_ip': mask_pii(data, 'ip'),
        'masked_device_id': mask_pii(data, 'device_id'),
        'locale': data['locale'],
        'app_version': data['app_version'],
        'create_date': data['create_date']
    }
