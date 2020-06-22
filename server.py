from socket import *

PORT = 9000
SERVER = '127.0.0.1' # Để test thì đổi IP này
FORMAT = 'utf-8'

#hàm xử lí request từ Client
def handleClient(client):
    request = client.recv(1024) #nhận request
    if request:
        request = request.decode(FORMAT) #decode to UTF-8
    else: #dont receive any requests, then return
        print("Not received any request\r\n")
        return
    print("Client request: \r\n" + request)
    str_list = request.split(' ') #tách chuỗi
    method = str_list[0]               
    if method == "GET": #xử lí method GET
        req_file = str_list[1] #tên file
        req_file = req_file.lstrip('/')
        req_file = req_file.replace("%20", " ")
        if (req_file == ''): #nếu không có tên file thì mặc định là index.html
            req_file = 'index.html'
        try:
            file = open(req_file, 'rb')
            response = file.read() #đọc nội dung file vào response
            file.close()
            header = "HTTP/1.1 200 OK\r\n" #header của response
            if req_file.endswith(".html"): #gắn vào header Content Type
                header += "Content-Type: text/html\r\n\r\n"
            elif req_file.endswith(".css"):
                header += "Content-Type: text/css\r\n\r\n"
            else:
                header += "Content=Type: */*\r\n\r\n"
        except Exception: #file không tồn tại
            header = "HTTP/1.1 404 Not Found\r\n\r\n" #header 404
            file = open("404.html", "rb")
            response = file.read() #đọc file 404.html vào response
            file.close()
        final_res = header.encode(FORMAT) #encode
        final_res += response #final response 
        client.send(final_res) #gửi response cho Client
    elif method == "POST": #xử lí method POST
        str_split = request.split('\n') #xử lí chuỗi để lấy username và password
        loginInfo = str_split[-1]
        username = loginInfo.split('&')[0]
        password = loginInfo.split('&')[1]
        username = username[9:]
        password = password[9:]
        if username == "admin" and password == "admin": #đúng -> chuyển hướng sang info.html
            header = "HTTP/1.1 301 Moved Permanently\r\nLocation: /info.html\r\n" #header của HTTP Redirection
            client.send(header.encode(FORMAT))  
        else: #sai -> báo lỗi 404
            header = "HTTP/1.1 404 Not Found\r\n\r\n"
            file = open("404.html", "rb")
            response = file.read()
            file.close()
            final_res = header.encode(FORMAT)
            final_res += response
            client.send(final_res)

#hàm khởi tạo Server và lắng nghe các kết nối
def startServer():
    serversocket = socket(AF_INET, SOCK_STREAM) #Khởi tạo socket
    try :
        serversocket.bind((SERVER, PORT)) #gán IP Address và Port
        serversocket.listen(5) #lắng nghe kết nối, hàng chờ tối đa 5
        print("Server is listening at http://" + SERVER + ":" + str(PORT))
        while(1):
            conn, address = serversocket.accept() #chấp nhận kết nối từ Client
            print("Connected to " + str(address))
            handleClient(conn) #gọi hàm để xử lí request
            conn.close()    #đóng kết nối đến Client và xử lí các request khác
    except KeyboardInterrupt:
        print("\nShutting down...\n")
    except Exception as exc:
        print("Error:\n")
        print(exc)
 
    print("Server is closing...")
    serversocket.close()

startServer()