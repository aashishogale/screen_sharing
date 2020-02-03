import asyncio
import datetime
import random
import websockets
import io
import base64
import pyscreenshot as ImageGrab


connected = set()
# async def time(websocket, path):
#     print(websocket)
#     while True:
#         now = datetime.datetime.utcnow().isoformat() + "Z"
#         await websocket.send(now)
#         await asyncio.sleep(random.random() * 3)

async def image(websocket, path):
    print(websocket)
    connected.add(websocket)

    while True:
        from threading import Thread
        from zlib import compress
        from socket import socket
        from mss import mss


        WIDTH = 1366
        HEIGHT = 768


      
    #     with mss(display=':0') as sct:
    # # The region to capture
    #         rect = {'top': 0, 'left': 0, 'width': WIDTH, 'height': HEIGHT}

    #         while 'recording':
    #         # Capture the screen
    #             img = sct.grab(rect)
    #         # Tweak the compression level here (0-9)
    #             pixels = compress(img.rgb, 6)

    #         # Send the size of the pixels length
    #             size = len(pixels)
    #             size_len = (size.bit_length() + 7) // 8
    #             # await websocket.send(bytes([size_len]))

    #         # Send the actual pixels length
    #             size_bytes = size.to_bytes(size_len, 'big')
    #             # await websocket.send(size_bytes)
    #         # Send pixels
    #             await websocket.send(img.rgb)

        buffer = io.BytesIO()

        im=ImageGrab.grab()
        im.save(buffer,quality=20,optimize=True, format='PNG')
        im.close()

        b64_str = base64.b64encode(buffer.getvalue())
        await asyncio.wait([websocket.send(b64_str) for ws in connected])

        # await websocket.send(b64_str)


        # def main(host='', port=8001):
        #     sock = socket()
        #     sock.bind((host, port))
        #     print(host, "host")
        #     print(sock)
        #     try:
        #         sock.listen(5)
        #         print('Server started.')
        #         while 'connected':
        #             print ("here")
        #             conn, addr = sock.accept()
        #             print('Client connected IP:', addr)
        #             thread = Thread(target=retreive_screenshot, args=(conn,sock,))
        #             thread.start()
        #             return render_template("view_screen.html")
        #     except OSError as e:
        #         sock.close()
        #         main()
        #     except Exception as e:
        #         sock.close()
        #         main()
        #         return render_template("view_screen.html")
     
       
        #     finally:
        #         sock.close()
        #         main()
        #         return render_template("view_screen.html")
        # try:
        #     main()

        # except Exception as e:
        #     return render_template("view_screen.html")

start_server = websockets.serve(image, "192.168.0.136", 8001)
print ("jhfdjhf")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
