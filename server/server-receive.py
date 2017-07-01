import io
import socket
import struct
from PIL import Image

#############################################################################
# CODE TO CONVERT TO ASCII
#############################################################################
ASCII_CHARS = [" ",".","'","-",":",";","!","~","*","+","?","r","t","e","x","z","m","6","8","g","%","#","W","M","B","@",]

def scale_image(image, new_width=180):
    (original_width, original_height) = image.size
    aspect_ratio = original_height/float(original_width)
    #To counter general issue that ascii characters are tall and not square
    new_height = int(aspect_ratio * new_width)*6/11
    new_image = image.resize((new_width, new_height))
    return new_image

def convert_to_grayscale(image):
    return image.convert('L')

def map_pixels_to_ascii_chars(image, range_width=11):
    pixels_in_image = list(image.getdata())
    pixels_to_chars = [ASCII_CHARS[pixel_value/range_width] for pixel_value in
            pixels_in_image]

    return "".join(pixels_to_chars)

def convert_image_to_ascii(image, new_width=180):
    #Use size of image a width, what we pass from camera is what we want in return
    new_width=image.size[0]
    #Reference returned image new size as it could be updated along hte way
    image = scale_image(image, image.size[0])
    image = convert_to_grayscale(image)

    pixels_to_chars = map_pixels_to_ascii_chars(image)
    len_pixels_to_chars = len(pixels_to_chars)

    image_ascii = [pixels_to_chars[index: index + new_width] for index in
            xrange(0, len_pixels_to_chars, new_width)]

    return "\n".join(image_ascii)

#############################################################################
# CODE TO RECEIVE IMAGE
#############################################################################
# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
def receive_video_stream(port):
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', int(port)))
    server_socket.listen(0)
    print("LISTENING ON PORT:"+port)
    # Accept a single connection and make a file-like object out of it
    connection = server_socket.accept()[0].makefile('rb')
    try:
        while True:
            # Read the length of the image as a 32-bit unsigned int. If the
            # length is zero, quit the loop
            image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
            if not image_len:
                break
            # Construct a stream to hold the image data and read the data from the connection
            image_stream = io.BytesIO()
            image_stream.write(connection.read(image_len))
            # Rewind the stream, open as PIL image and do process it
            image_stream.seek(0)
            image = Image.open(image_stream)
            print('Sent Image. Size is %dx%d' % image.size)
            ##### SAVE TO ASCII
            ascii = convert_image_to_ascii(image)
            text_file = open("/var/www/html/ascii-text.txt", "w")
            text_file.write(ascii)
            text_file.close()
    finally:
        connection.close()
        server_socket.close()


if __name__=='__main__':
    import sys

    port  = sys.argv[1]
    receive_video_stream(port)