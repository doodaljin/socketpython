from socket import *
import time

PORT = 9000
SERVER = '127.0.0.1'
FORMAT = 'utf-8'

def createServer():
    serversocket = socket(AF_INET, SOCK_STREAM)
    try :
        serversocket.bind((SERVER, PORT))
        serversocket.listen(5)
        while(1):
            conn, address = serversocket.accept()
            print("connected to " + str(address))
            request = conn.recv(1024)
            if request:
                request = request.decode(FORMAT)
            else:
                print("not received")
                continue 
            print(request)
            str_list = request.split(' ')
            method = str_list[0]               
            if method == "GET":
                req_file = str_list[1]
                req_file = req_file.lstrip('/')
                if (req_file == ''):
                    req_file = 'index.html'
                try:
                    file = open(req_file, 'rb')
                    response = file.read()
                    file.close()
                    header = "HTTP/1.1 200 OK\r\n"
                    if req_file.endswith(".ico"):
                        header += "Content-Type: image/ico\r\n\r\n"
                    elif req_file.endswith(".html"):
                        header += "Content-Type: text/html\r\n\r\n"
                    elif req_file.endswith(".jpg"):
                        header += "Content-Type: image/jpg\r\n\r\n"
                    elif req_file.endswith(".css"):
                        header += "Content-Type: text/css\r\n\r\n"
                except Exception as e:
                    header = "HTTP/1.1 404 Not Found\r\n\r\n"
                    file = open("404.html", "rb")
                    response = file.read()
                    file.close()
                final_res = header.encode(FORMAT)
                final_res += response
                conn.send(final_res)   
            else:
                str_split = request.split('\n')
                loginInfo = str_split[-1]
                username = loginInfo.split('&')[0]
                password = loginInfo.split('&')[1]
                username = username[9:]
                password = password[9:]
                if username == "admin" and password == "admin":
                    header = "HTTP/1.1 301 Moved Permanently\r\nLocation: /info.html\r\n"
                    conn.send(header.encode(FORMAT))  
                else:
                    header = "HTTP/1.1 404 Not Found\r\n\r\n"
                    file = open("404.html", "rb")
                    response = file.read()
                    file.close()
                    final_res = header.encode(FORMAT)
                    final_res += response
                    conn.send(final_res)
            conn.close()    
    except KeyboardInterrupt :
        print("\nShutting down...\n")
    
    print("close")
    serversocket.close()

print(SERVER)
createServer()