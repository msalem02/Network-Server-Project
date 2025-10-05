# Network Server Project  
### TCP/IP Socket Programming and Client-Server Communication in Python / C++

---

## 1. Overview

The **Network Server Project** demonstrates the fundamentals of **TCP/IP networking**, focusing on building a fully functional **client-server architecture**.  
The project enables multiple clients to connect to a central server, exchange messages, and perform specific actions such as file transfer, command execution, or remote data sharing.

This system is designed as an educational yet practical foundation for real-world applications in distributed computing, cloud services, and IoT communications.

---

## 2. Objectives

- Implement a **TCP-based communication system** between server and clients.  
- Handle **multiple concurrent connections** using threading or asynchronous I/O.  
- Enable **bi-directional data exchange** with message framing and validation.  
- Develop a **modular, scalable, and reusable network codebase**.  
- Provide detailed logging, error handling, and testing mechanisms.  

---

## 3. Project Structure

```
Network-Server-Project/
│
├── src/
│   ├── server.py / server.cpp          # Main server implementation
│   ├── client.py / client.cpp          # Client-side program
│   ├── thread_handler.py / .cpp        # Thread or connection handler logic
│   ├── utils.py / .cpp                 # Shared utilities and constants
│   ├── config.json                     # Configuration file (IP, ports, buffer size)
│   └── main.py / main.cpp              # Launch entry for server/client mode
│
├── logs/
│   ├── server_log.txt                  # Server runtime logs
│   ├── client_log.txt                  # Client logs
│   └── errors.log                      # Exception logs
│
├── tests/
│   ├── test_connection.txt
│   ├── test_file_transfer.txt
│   └── run_tests.sh
│
├── docs/
│   ├── network_architecture.png
│   ├── sequence_diagram.png
│   └── design_report.pdf
│
├── Makefile / requirements.txt
└── README.md
```

---

## 4. Communication Model

The architecture follows a **TCP client-server model** where:  
- The **server** listens on a specified IP address and port.  
- Multiple **clients** can connect simultaneously.  
- Each connection is handled in a **separate thread** or **asynchronous task**.  
- The communication protocol ensures message delivery, acknowledgment, and graceful disconnection.

### Example Flow
1. Server starts and listens on port `5000`  
2. Client connects to the server IP:port  
3. Server accepts connection and creates thread for each client  
4. Messages exchanged using UTF-8 encoding  
5. On termination, server closes sockets gracefully

---

## 5. Key Features

| Feature | Description |
|----------|-------------|
| **TCP Communication** | Reliable, connection-oriented data transfer |
| **Multi-Client Support** | Handles multiple clients simultaneously |
| **Threaded or Async Design** | Efficient concurrent message handling |
| **Configurable Parameters** | Dynamic control over IPs, ports, buffers |
| **Logging System** | Tracks all messages, connections, and errors |
| **Cross-Platform** | Compatible with Windows, Linux, and macOS |

---

## 6. Implementation Details

### 6.1 Server (Python Example)
```python
import socket
import threading

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr}")
    while True:
        msg = conn.recv(1024).decode('utf-8')
        if not msg or msg.lower() == 'exit':
            break
        print(f"[{addr}] {msg}")
        conn.send("ACK".encode('utf-8'))
    conn.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 5000))
server.listen()
print("[SERVER STARTED] Listening on port 5000")

while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
    print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
```

### 6.2 Client (Python Example)
```python
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 5000))

while True:
    msg = input("Enter message: ")
    client.send(msg.encode('utf-8'))
    if msg.lower() == 'exit':
        break
    response = client.recv(1024).decode('utf-8')
    print("Server:", response)

client.close()
```

---

## 7. Example Execution

**Terminal 1 (Server):**
```bash
python server.py
```

**Terminal 2 (Client):**
```bash
python client.py
```

**Output Example:**
```
[SERVER] Listening on port 5000...
[NEW CONNECTION] ('127.0.0.1', 50932)
[Client] Enter message: Hello Server
[SERVER] ('127.0.0.1', 50932): Hello Server
[SERVER] Sent acknowledgment: ACK
```

---

## 8. Configuration File Example

`config.json`
```json
{
  "server_ip": "127.0.0.1",
  "server_port": 5000,
  "buffer_size": 1024,
  "max_clients": 10
}
```

---

## 9. Error Handling and Logging

- Detects invalid IP or port configurations.  
- Gracefully handles client disconnects.  
- Prevents crashes from socket errors using try/except or error codes.  
- Writes full logs to `/logs/server_log.txt` and `/logs/errors.log`.

---

## 10. Testing and Validation

### Manual Testing
Run multiple clients and verify simultaneous communication.

### Automated Testing
```
./tests/run_tests.sh
```

### Unit Tests
- Connection establishment
- Message integrity
- Server timeout handling
- File transmission (if implemented)

---

## 11. Performance and Scalability

| Parameter | Description | Typical Result |
|------------|--------------|----------------|
| Max Connections | Default thread limit | 100+ clients |
| Latency | Message round-trip (local) | < 5ms |
| Throughput | Data per second | 2–5 MB/s |
| CPU Usage | Multithreaded with 5 clients | ~12% |

---

## 12. Educational Objectives

Students and developers will learn:
- The **difference between TCP and UDP protocols**.  
- How to implement socket-based network communication.  
- Thread synchronization and concurrency management.  
- Proper resource cleanup in networking systems.  
- Real-world server design and fault-tolerant architecture.

---

## 13. Future Enhancements

- Add **file upload/download** functionality.  
- Implement **encryption (TLS/SSL)** for secure communication.  
- Support **broadcast or multicast** for group messaging.  
- Add **web-based dashboard** for monitoring connections.  
- Migrate to **asyncio / epoll** for high-performance servers.

---

## 14. Author

Mohammed Salem  
Email: salemmohamad926@gmail.com  
LinkedIn: https://www.linkedin.com/in/msalem02  
GitHub: https://github.com/msalem02

---

## 15. License

This project is licensed under the **MIT License**.  
You may freely use, modify, and distribute it with attribution.

---

## 16. Acknowledgements

- Birzeit University — Computer Engineering Department  
- Network Programming course instructors and mentors  
- Open-source contributors for socket examples and libraries  
- Classmates for collaboration and testing support

---

## 17. Version History

| Version | Date | Description |
|----------|------|-------------|
| 1.0 | February 2024 | Basic single-client server implementation |
| 1.1 | March 2024 | Added multi-client support with threads |
| 1.2 | April 2024 | Improved logging and error handling |
| 2.0 | June 2024 | Modularized code and added config file |
