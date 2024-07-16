import binascii

#kezdő és véget karakter(string) formában várja, a contenten bytes-ként
def calc_checksum(start_char, content, end_char):
    start_bytes = bytes(start_char, 'ascii')
    end_bytes = bytes(end_char, 'ascii')
    checksum = sum(start_bytes + content + end_bytes) % 256
    checksum_bytes = checksum.to_bytes(1, 'big')
    checksum_hex = binascii.hexlify(checksum_bytes)

    return checksum_hex