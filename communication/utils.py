import binascii

def calc_checksum(content):
    checksum = sum(content) % 256
    checksum_bytes = checksum.to_bytes(1, 'big')
    checksum_hex = binascii.hexlify(checksum_bytes)

    return checksum_hex