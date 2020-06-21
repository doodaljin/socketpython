from socket import *

PORT = 9000
SERVER = '127.0.0.1' # Để test thì đổi IP này
FORMAT = 'utf-8'

def handleClient(client):
    request = client.recv(1024)
    if request:
        request = request.decode(FORMAT)
    else:
        print("Not received any request\r\n")
        return
    print("Client request: \r\n" + request)
    str_list = request.split(' ')
    method = str_list[0]               
    if method == "GET":
        req_file = str_list[1]
        req_file = req_file.lstrip('/')
        req_file = req_file.replace("%20", " ")
        if (req_file == ''):
            req_file = 'index.html'
        try:
            file = open(req_file, 'rb')
            response = file.read()
            file.close()
            header = "HTTP/1.1 200 OK\r\n"
            if req_file.endswith(".html"):
                header += "Content-Type: text/html\r\n\r\n"
            elif req_file.endswith(".css"):
                header += "Content-Type: text/css\r\n\r\n"
            else:
                header += "Content=Type: */*\r\n\r\n"
        except Exception: 
            header = "HTTP/1.1 404 Not Found\r\n\r\n"
            file = open("404.html", "rb")
            response = file.read()
            file.close()
        final_res = header.encode(FORMAT)
        final_res += response
        client.send(final_res)
    elif method == "POST": 
        str_split = request.split('\n')
        loginInfo = str_split[-1]
        username = loginInfo.split('&')[0]
        password = loginInfo.split('&')[1]
        username = username[9:]
        password = password[9:]
        if username == "admin" and password == "admin":
            header = "HTTP/1.1 301 Moved Permanently\r\nLocation: /info.html\r\n"
            client.send(header.encode(FORMAT))  
        else:
            header = "HTTP/1.1 404 Not Found\r\n\r\n"
            file = open("404.html", "rb")
            response = file.read()
            file.close()
            final_res = header.encode(FORMAT)
            final_res += response
            client.send(final_res)

def startServer():
    serversocket = socket(AF_INET, SOCK_STREAM)
    try :
        serversocket.bind((SERVER, PORT))
        serversocket.listen(5)
        print("Server is listening at http://" + SERVER + ":" + str(PORT))
        while(1):
            conn, address = serversocket.accept()
            print("Connected to " + str(address))
            handleClient(conn)
            conn.close()    
    except KeyboardInterrupt:
        print("\nShutting down...\n")
    except Exception as exc:
        print("Error:\n")
        print(exc)
 
    print("Server is closing...")
    serversocket.close()

startServer()