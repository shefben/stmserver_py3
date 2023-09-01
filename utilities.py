def ljust_bytes(data, length, fill_byte=b'\x00'):
    if len(data) >= length:
        return data
    padding = length - len(data)
    return data + (fill_byte * padding)

# Usage
# replace_ip = utilities.ljust_bytes(server_ip, 16, b'\x00')