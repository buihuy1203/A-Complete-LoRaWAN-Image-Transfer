import binascii

def list_to_hex(hex_string):
    merge_string = ''.join(hex_string)
    print(merge_string)
    return merge_string
def hex_to_image(hex_string):
    # Xóa bỏ ký tự '0x' nếu có
    if hex_string.startswith('0x') or hex_string.startswith('0X'):
        hex_string = hex_string[2:]
    hex_string=hex_string.strip()
    hex_string=hex_string.replace(' ', '')
    hex_string=hex_string.replace('\n', '')
    print(len(hex_string))
    # Giải mã chuỗi hex thành dữ liệu nhị phân
    binary_data = binascii.unhexlify(hex_string)
    # Lưu dữ liệu nhị phân vào một tệp ảnh tạm thời
    return binary_data
