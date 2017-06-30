import io
import socket
import struct
from PIL import Image

#############################################################################
# CODE TO CONVERT TO ASCII
#############################################################################
ASCII_CHARS = [
    " ",
    ".",
    "'",
    "-",
    ":",
    ";",
    "!",
    "~",
    "*",
    "+",
    "e",
    "m",
    "6",
    "8",
    "g",
    "#",
    "W",
    "M",
    "@",
]

def scale_image(image, new_width=200):
    """Resizes an image preserving the aspect ratio.
    """
    (original_width, original_height) = image.size
    aspect_ratio = original_height/float(original_width)
    new_height = int(aspect_ratio * new_width)*6/11
    new_image = image.resize((new_width, new_height))
    return new_image

def convert_to_grayscale(image):
    return image.convert('L')

def map_pixels_to_ascii_chars(image, range_width=15):
    """Maps each pixel to an ascii char based on the range
    in which it lies.

    0-255 is divided into 11 ranges of 25 pixels each.
    """

    pixels_in_image = list(image.getdata())
    pixels_to_chars = [ASCII_CHARS[pixel_value/range_width] for pixel_value in
            pixels_in_image]

    return "".join(pixels_to_chars)

def convert_image_to_ascii(image, new_width=200):
    image = scale_image(image)
    image = convert_to_grayscale(image)

    pixels_to_chars = map_pixels_to_ascii_chars(image)
    len_pixels_to_chars = len(pixels_to_chars)

    image_ascii = [pixels_to_chars[index: index + new_width] for index in
            xrange(0, len_pixels_to_chars, new_width)]

    return "\n".join(image_ascii)

def handle_image_conversion(image_filepath):
    image_ascii = convert_image_to_ascii(image)
    print image_ascii

#############################################################################
# CODE TO RECEIVE IMAGE
#############################################################################
# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(0)
print("LISTENING")
# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')
try:
    while True:
        # Read the length of the image as a 32-bit unsigned int. If the
        # length is zero, quit the loop
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            break
        # Construct a stream to hold the image data and read the image
        # data from the connection
        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))
        # Rewind the stream, open it as an image with PIL and do some
        # processing on it
        image_stream.seek(0)
        image = Image.open(image_stream)
        print('Image is %dx%d' % image.size)
        #image.verify()
        #print('Image is verified')
        #imagetoconverttoascii = image.convert('RGB')
        ##### SAVE TO ASCII
        ascii = convert_image_to_ascii(image)
        print ascii
        text_file = open("/var/www/html/ascii-text.txt", "w")
        text_file.write(ascii)
        text_file.close()
        #imagetoconverttoascii.save("/usr/imagetoconverttoascii.jpg")
        #print('Image is saved as imagetoconverttoascii.jpg')
	#image.save('imagetoconvert.jpg')
finally:
    connection.close()
    server_socket.close()
