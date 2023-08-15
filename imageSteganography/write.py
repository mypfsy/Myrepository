from PIL import Image


def str_to_bin(string):
    binary = [("0" * (8 - len(str(bin(ord(ch)))[2:])) + str(bin(ord(ch)))[2:]) for ch in string]
    return "".join(binary)


def make_image_even(image):
    pixels = list(image.getdata())
    evenPixels = [(r >> 1 << 1, g >> 1 << 1, b >> 1 << 1, a >> 1 << 1,) for [r, g, b, a] in pixels]
    evenImage = Image.new(image.mode, image.size)
    evenImage.putdata(evenPixels)
    return evenImage


def encode_image(image, binary_data, byte_length):
    evenImage = make_image_even(image)
    if len(binary_data) > len(image.getdata()) * 4 - 24:
        print(f"byte = {byte_length}, size out of range, the max byte = {int(len(image.getdata()) * 4 / 8) - 3} byte")
        return 0
    byte_length_bin = (24 - (len(bin(byte_length)) - 2)) * '0' + bin(byte_length).replace("0b", '')
    encodePixels = list(evenImage.getdata())[:-6] + \
                   [(r + int(byte_length_bin[index * 4 + 0]),
                     g + int(byte_length_bin[index * 4 + 1]),
                     b + int(byte_length_bin[index * 4 + 2]),
                     a + int(byte_length_bin[index * 4 + 3])
                    ) for index, (r, g, b, a) in
                   enumerate(list(evenImage.getdata())[-6:])]
    encodePixels = [(r + int(binary_data[index * 4 + 0]),
                     g + int(binary_data[index * 4 + 1]),
                     b + int(binary_data[index * 4 + 2]),
                     a + int(binary_data[index * 4 + 3])
                     ) if index * 4 < len(binary_data) else (r, g, b, a) for index, (r, g, b, a) in
                    enumerate(encodePixels)]
    encodeImage = Image.new(evenImage.mode, evenImage.size)
    encodeImage.putdata(encodePixels)
    print(f"A total of {byte_length} byte")
    print(f"max byte = {int(len(image.getdata()) * 4 / 8) - 3} byte")
    return encodeImage


if __name__ == "__main__":
    with open("text.txt", 'r', encoding="utf-8") as f:
        text = f.read()
    byte_length = len(text)
    image = Image.open("3ll3wd.jpg")
    rgbaImage = image.convert("RGBA")
    encodeImage = encode_image(rgbaImage, str_to_bin(text), byte_length)
    box = rgbaImage.getbbox()
    encodeImage = encodeImage.crop(box)
    encodeImage.save("3ll3wd_en.png")
