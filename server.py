import os
import base64
from socket import *

# Server configuration
serverPort = 6060  # Port number
serverSocket = socket(AF_INET, SOCK_STREAM)  # Create socket (TCP)
serverSocket.bind(('', serverPort))  # Bind socket to address
serverSocket.listen(1)  # Listen for incoming connections (1 at a time)

print('The server is ready to receive')
print(serverSocket.getsockname())  # Print server address


# Function to find image file based on the provided name
def find_image(image_name):
    # Check if image_name already has an extension
    if not any(image_name.endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif']):
        extensions = ['png', 'jpg', 'jpeg', 'gif']  # List of image file extensions to check
        for ext in extensions:
            file_path = f"{image_name}.{ext}"
            if os.path.isfile(file_path):
                try:
                    with open(file_path, "rb") as img_file:
                        print(f"Found image at: {file_path}")
                        return img_file.read(), f"image/{ext}"  # Return the file content and extension
                except FileNotFoundError:
                    continue
    else:
        try:
            with open(image_name, "rb") as img_file:
                ext = image_name.split('.')[-1]
                return img_file.read(), f"image/{ext}"
        except FileNotFoundError:
            print(f"File not found: {image_name}")

    print(f"Image not found for {image_name}")
    return None, None  # Return None if no file is found

# Function to send HTTP response to the client socket
def send_response(client_socket, content, content_type, is_binary=False):
    response_header = 'HTTP/1.1 200 OK\r\n'  # Initial response header
    if is_binary:
        response_header += f"Content-Type: {content_type}\r\n"  # Add content type for binary data
        response_header += 'Content-Length: ' + str(len(content)) + '\r\n'  # Add content length
        response_header += '\r\n'  # End of header
        client_socket.send(response_header.encode() + content)  # Send header and content
    else:
        response_header += "Content-Type: text/html\r\n\r\n"  # Add content type for HTML
        full_response = response_header + content  # Combine header and content
        client_socket.send(full_response.encode())  # Send response

# Function to handle 404 Not Found error
def handle_not_found(client_socket):
    client = ip + ":" + str(port)  # Client IP and port
    # HTML error message for 404
    html_error = f"""
                   <!DOCTYPE html>
                   <html lang="">
                   <head>
                     <title>Error 404</title>
                     <link rel="stylesheet" type="text/css" href="style.css">
                   </head>
                   <body>
                     <h1 style="color:red">The file is not found</h1>
                     <h2><strong>Group Members:</strong></h2>
                     <ul class="boldlist">
                       <li>Mohammed Salem : 1203022</li>
                       <li>Yousef Eyad : 1201742 </li>
                     </ul>
                     <p>IP and port number of the client: {client}</p>
                   </body>
                   </html>
               """
    # Send 404 response with HTML error message
    client_socket.send(bytes("HTTP/1.1 404 NOT FOUND\r\n", "utf-8"))
    client_socket.send(bytes("Content-Type: text/html\r\n", "utf-8"))
    client_socket.send(bytes("\r\n", "utf-8"))
    client_socket.send(bytes(html_error, "utf-8"))
    print("SENT HTML_ERROR\r\n\n")  # Print confirmation


# Main server loop
while True:
    clientSocket, addr = serverSocket.accept()  # Accept incoming connection
    ip = addr[0]  # Client IP
    port = addr[1]  # Client port
    print('Got Connection from, IP: ' + ip + ", Port: " + str(port))  # Print client info

    full_request = clientSocket.recv(1024).decode()  # Receive request from client
    print(full_request)  # Print request

    # Process request
    if len(full_request) != 0:
        lines = full_request.splitlines()  # Split request into lines
        first_line = lines[0]  # First line of request
        method, path = first_line.split()[0], first_line.split()[1]  # Extract method and path

        # Handle POST request to fetch image
        if method == 'POST' and path == '/find-image':
            body = full_request.split('\r\n\r\n')[1]  # Extract body of POST request
            image_name = body.split('=')[1]  # Extract image name from POST data
            image_data, ext = find_image(image_name)  # Find image data and extension
            if image_data:
                # Embed image in HTML and send response
                html_content = f'<html><body><h1>Image Display</h1><img src="data:image/{ext};base64,{base64.b64encode(image_data).decode()}" /></body></html>'
                send_response(clientSocket, html_content, f"text/html")
            else:
                handle_not_found(clientSocket)  # Handle 404 error

        # Handle GET requests
        elif path in ['/', '/en', '/index.html', '/main_en.html']:
            # Send main HTML content for English
            with open("main_en.html", "rb") as file:
                file_content = file.read()
            clientSocket.send(bytes("HTTP/1.1 200 OK\r\n", "utf-8"))
            clientSocket.send(bytes("Content-Type: text/html\r\n", "utf-8"))
            clientSocket.send(bytes("\r\n", "utf-8"))
            clientSocket.send(file_content)
            print("SENT HTML_EN\r\n\n")

        elif path in ['/ar', '/main_ar.html']:
            # Send main HTML content for Arabic
            with open("main_ar.html", "rb") as file:
                file_content = file.read()
            clientSocket.send(bytes("HTTP/1.1 200 OK\r\n", "utf-8"))
            clientSocket.send(bytes("Content-Type: text/html\r\n", "utf-8"))
            clientSocket.send(bytes("\r\n", "utf-8"))
            clientSocket.send(file_content)
            print("SENT HTML_AR\r\n\n")

        # Handle CSS file request
        elif path in ['/style.css', '/.css']:
            with open("style.css", "r") as file:
                file_content = file.read()
            # Send CSS file content
            clientSocket.send(bytes("HTTP/1.1 200 OK\r\n", "utf-8"))
            clientSocket.send(bytes("Content-Type: text/css\r\n", "utf-8"))
            clientSocket.send(bytes("\r\n", "utf-8"))
            clientSocket.send(bytes(file_content, "utf-8"))
            print("SENT STYLE_CSS\r\n\n")

        # Handle PNG image request
        elif path in ['/bzu-logo.png', '/.png']:
            with open("bzu-logo.png", "rb") as file:
                file_content = file.read()
            # Send PNG image content
            clientSocket.send(bytes("HTTP/1.1 200 OK\r\n", "utf-8"))
            clientSocket.send(bytes("Content-Type: image/png\r\n", "utf-8"))
            clientSocket.send(bytes("\r\n", "utf-8"))
            clientSocket.send(file_content)
            print("SENT BZU_CIRCLE_PNG\r\n\n")

        # Handle JPEG image request
        elif path in ['/Birzeit-University-campus.jpg', '/.jpg']:
            with open("Birzeit-University-campus.jpg", "rb") as file:
                file_content = file.read()
            # Send JPEG image content
            clientSocket.send(bytes("HTTP/1.1 200 OK\r\n", "utf-8"))
            clientSocket.send(bytes("Content-Type: image/jpeg\r\n", "utf-8"))
            clientSocket.send(bytes("\r\n", "utf-8"))
            clientSocket.send(file_content)
            print("SENT BZU_UNI_JPEG\r\n\n")

        # Handle redirection to external URLs
        elif path == '/itc':
            clientSocket.send(bytes("HTTP/1.1 307 temporary Redirect\r\n", "utf-8"))
            clientSocket.send(bytes("Content-Type:\r\n", "utf-8"))
            clientSocket.send(bytes("location: https://itc.birzeit.edu\r\n", "utf-8"))
            print("REDIRECT TO ITC \r\n\n")

        elif path == '/so':
            clientSocket.send(bytes("HTTP/1.1 307 temporary Redirect\r\n", "utf-8"))
            clientSocket.send(bytes("Content-Type:\r\n", "utf-8"))
            clientSocket.send(bytes("location: https://stackoverflow.com\r\n", "utf-8"))
            print("REDIRECT TO STACKOVERFLOW\r\n\n")

        # Handle request for form HTML file
        elif path in ['/myform.html', '/myform', '/form', '/.html']:
            with open("myform.html", "rb") as file:
                file_content = file.read()
            # Send form HTML content
            clientSocket.send(bytes("HTTP/1.1 200 OK\r\n", "utf-8"))
            clientSocket.send(bytes("Content-Type: text/html\r\n", "utf-8"))
            clientSocket.send(bytes("\r\n", "utf-8"))
            clientSocket.send(file_content)
            print("SENT HTML_MYFORM\r\n\n")

        else:
            handle_not_found(clientSocket)  # Handle 404 error for unknown paths
    clientSocket.close()  # Close client socket after handling request
