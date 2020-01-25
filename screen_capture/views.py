from flask.views import MethodView
from flask import Response
import json
from flask import render_template, redirect
import requests


class ShowViewScreen(MethodView):
    def get(self):
        try:
            return render_template("view_screen.html")
        except ConnectionResetError as e:
            return redirect("/")
        

class StartServer(MethodView):
    def get(self):
        from threading import Thread
        from zlib import compress
        from socket import socket
        from mss import mss


        WIDTH = 1366
        HEIGHT = 768


        def retreive_screenshot(conn, sock):
            with mss(display=':0') as sct:
        # The region to capture
                rect = {'top': 0, 'left': 0, 'width': WIDTH, 'height': HEIGHT}

                while 'recording':
                # Capture the screen
                    img = sct.grab(rect)
                # Tweak the compression level here (0-9)
                    pixels = compress(img.rgb, 6)

                # Send the size of the pixels length
                    size = len(pixels)
                    size_len = (size.bit_length() + 7) // 8
                    conn.send(bytes([size_len]))

                # Send the actual pixels length
                    size_bytes = size.to_bytes(size_len, 'big')
                    conn.send(size_bytes)
                # Send pixels
                    conn.sendall(pixels)



        def main(host='', port=8001):
            sock = socket()
            sock.bind((host, port))
            print(host, "host")
            print(sock)
            try:
                sock.listen(5)
                print('Server started.')
                while 'connected':
                    print ("here")
                    conn, addr = sock.accept()
                    print('Client connected IP:', addr)
                    thread = Thread(target=retreive_screenshot, args=(conn,sock,))
                    thread.start()
                    return render_template("view_screen.html")
            except OSError as e:
                sock.close()
                main()
            except Exception as e:
                sock.close()
                main()
                return render_template("view_screen.html")
     
       
            finally:
                sock.close()
                main()
                return render_template("view_screen.html")
        try:
            main()

        except Exception as e:
            return render_template("view_screen.html")
        

class StartClient(MethodView):
    def get(self):
        from socket import socket
        from zlib import decompress
        import pygame

        WIDTH = 1366
        HEIGHT = 768


        def recvall(conn, length):
            """ Retreive all pixels. """

            buf = b''
            while len(buf) < length:
                data = conn.recv(length - len(buf))
                if not data:
                    return data
                buf += data
            return buf


        def main(host='192.168.0.136', port=8001):
            pygame.init()
            screen = pygame.display.set_mode((WIDTH, HEIGHT))
            clock = pygame.time.Clock()
            watching = True    

            sock = socket()
            print (host)
            
            sock.connect((host, port))
            print(sock)
            try:
                while watching:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            watching = False
                            break

                    # Retreive the size of the pixels length, the pixels length and pixels
                    size_len = int.from_bytes(sock.recv(1), byteorder='big')
                    if not size_len:
                        pygame.quit()
                        break
                    # size = int.from_bytes(sock.recv(size_len), byteorder='big')
                    size = int.from_bytes(recvall(sock, size_len), byteorder='big')

                    pixels = decompress(recvall(sock, size))

                    # Create the Surface from raw pixels
                    img = pygame.image.fromstring(pixels, (WIDTH, HEIGHT), 'RGB')

                    # Display the picture
                    screen.blit(img, (0, 0))
                    pygame.display.flip()
                    clock.tick(60)
                pygame.quit()
                return render_template("view_screen.html")
    
            except OSError as e:
                print ("os")
                sock.close()
                main()  
                return render_template("view_screen.html")   
            finally:
                sock.close()
                return render_template("view_screen.html")
        try:
            main()
            return render_template("view_screen.html")
        except TypeError as e:
            print("type/")
            return render_template("view_screen.html")
        except ConnectionResetError as e:
            print("conn")
            return render_template("view_screen.html")
        except Exception as e:
            return render_template("view_screen.html")
        