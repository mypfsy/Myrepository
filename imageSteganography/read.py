from PIL import Image


byte_length = 0


def decode_image(image):
    global byte_length
    byte_length_bin = ''
    for RGBA in list(image.getdata())[-6:]:
        byte_length_bin += str(bin(RGBA[0]))[-1]
        byte_length_bin += str(bin(RGBA[1]))[-1]
        byte_length_bin += str(bin(RGBA[2]))[-1]
        byte_length_bin += str(bin(RGBA[3]))[-1]
    byte_length = int(byte_length_bin, 2)
    print(f"A total of {byte_length} byte")

    binary = ""
    for RGBA in list(image.getdata())[:2 * (byte_length)]:
        binary += str(bin(RGBA[0]))[-1]
        binary += str(bin(RGBA[1]))[-1]
        binary += str(bin(RGBA[2]))[-1]
        binary += str(bin(RGBA[3]))[-1]
    return binary


def bin_to_str(binary):
    string = ""
    for index in range(byte_length):
        chr_bin = binary[index * 8:index * 8 + 8]
        string += chr(int(chr_bin, 2))
    return string


if __name__ == "__main__":
    decode_binary = decode_image(Image.open("3ll3wd_en.png"))
    print(bin_to_str(decode_binary))
