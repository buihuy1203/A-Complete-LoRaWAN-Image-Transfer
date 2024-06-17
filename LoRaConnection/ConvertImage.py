import binascii

def image_to_hex(image_path):
    # Mở ảnh
    with open(image_path,'rb') as img:
        # Chuyển ảnh thành bytes
        img_byte_array = img.read()
        # Chuyển bytes thành chuỗi hex
        hex_string = binascii.hexlify(img_byte_array).decode('utf-8')
        return hex_string
def hex_to_list(hex_string):
    parts = [hex_string[i:i+240] for i in range(0, len(hex_string), 240)]
    return parts
