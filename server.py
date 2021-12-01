import socket


server = socket.create_server(("127.0.0.1", 8001))
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.listen(10)


try:
    while True:
        client_socket, address = server.accept()
        received_data = client_socket.recv(1024).decode('utf-8')
        print("Получили данные по сокету ", received_data)

        path = received_data.split(" ")[1]
        response =  f"HTTP1/1.1 200 OK\nContent-Type: text/html; charset=utf-8\n\n" \
                    f"Привет!<br />Path: {path}"

        client_socket.send(response.encode("utf-8"))
        client_socket.shutdown(socket.SHUT_RDWR)
except KeyboardInterrupt:
    server.shutdown(socket.SHUT_RDWR)
    server.close()