import io
import socket
import struct
import time
import picamera

########################################################################
# STREAM SEND CODE
########################################################################
# Connect a client socket to my_server:8000 (change my_server to the
# hostname of your server)
def send_video_stream(server, port, width, height):
    client_socket = socket.socket()
    #client_socket.connect(('pimatrix.westeurope.cloudapp.azure.com', 8000))
    client_socket.connect((server, int(port)))
    #client_socket.connect(('localhost', 8000))

    # Make a file-like object out of the connection
    connection = client_socket.makefile('wb')
    try:
        with picamera.PiCamera() as camera:
            camera.resolution = (int(width), int(height))
            # Start a preview and let the camera warm up for 1 second
            camera.start_preview()
            time.sleep(1)

            # Note the start time and construct a stream to hold image data
            # temporarily (we could write it directly to connection but in this
            # case we want to find out the size of each capture first to keep
            # our protocol simple)
            start = time.time()
            stream = io.BytesIO()
            for foo in camera.capture_continuous(stream, 'jpeg'):
                # Write the length of the capture to the stream and flush to
                # ensure it actually gets sent
                connection.write(struct.pack('<L', stream.tell()))
                connection.flush()
                # Rewind the stream and send the image data over the wire
                stream.seek(0)
                connection.write(stream.read())
                stream.seek(0)
                stream.truncate()
        # Write a length of zero to the stream to signal we're done
        connection.write(struct.pack('<L', 0))
    finally:
        connection.close()
        client_socket.close()


if __name__=='__main__':
    import sys

    server = sys.argv[1]
    port   = sys.argv[2]
    width  = sys.argv[3]
    height = sys.argv[4]
    send_video_stream(server, port, width, height)
