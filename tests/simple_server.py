import socket

HOST, PORT = '', 8080

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)
print('Serving HTTP on port {} ...'.format(PORT))
while True:
    client_connection, client_address = listen_socket.accept()
    request = client_connection.recv(1024)
    print(request)

    resp = {'dataversion': 155482806, 'mode': 1, 'temperature': 'C', 'scenes': [{'active': 0, 'id': 6, 'name': 'All belysning on', 'room': 0}, {'state': -1, 'id': 18, 'active': 1, 'comment': '', 'name': 'Garageporten on', 'room': 0}]}
    
    http_response = """\
    HTTP/1.1 200 OK

    {"scenes": [{"id": 1, "name": "hej"}], "devices": [{"altid": "16", "category": 3, "status": "0", "id": 46, "subcategory": 0, "comment": "_Appliance Module: ERROR: Unable to get any information on node", "commFailure": "1", "state": 2, "room": 11, "name": "Appliance Module", "parent": 1}]}
    """
    client_connection.sendall(http_response.encode())
    client_connection.close()

    #{'dataversion': 155482806, 'mode': 1, 'temperature': 'C', 'scenes': [{'active': 0, 'id': 6, 'name': 'All belysning on', 'room': 0}, {'state': -1, 'id': 18, 'active': 1, 'comment': '', 'name': 'Garageporten on', 'room': 0}]}



    
