# UDP Networking Project: Heartbeat & Pinger Systems


This project demonstrates **UDP-based communication** in Python through two systems:
1. A **Heartbeat system** for monitoring server availability.
2. A **UDP Pinger system** for measuring round-trip times (RTTs) and packet loss.


---


## 📂 Project Structure
```
.
├── Heartbeat_Client.py # Sends heartbeat signals to the server
├── UDP_Heartbeat_Server.py # Receives and acknowledges heartbeats
├── UDP_Pinger_Client.py # Sends ping messages and measures RTT
├── UDP_Pinger_Server.py # Simulates packet loss and responds to pings
└── README.md
```


---


## ⚡ Heartbeat System


### Files
- **Heartbeat_Client.py**
- **UDP_Heartbeat_Server.py**


### How It Works
- The **client** sends heartbeat packets with sequence numbers and timestamps at fixed intervals (default: 1 second).
- The **server** receives them and sends acknowledgments back.
- If the client misses 5 consecutive ACKs, it assumes the server is down and stops.


### Run Example
In two terminals:
```bash
# Terminal 1 (server)
python UDP_Heartbeat_Server.py


# Terminal 2 (client)
python Heartbeat_Client.py
```


---


## 📡 UDP Pinger System


### Files
- **UDP_Pinger_Client.py**
- **UDP_Pinger_Server.py**


### How It Works
- The **client** sends 10 UDP ping messages to the server.
- The **server** randomly drops ~40% of packets (to simulate unreliable networks).
- The client calculates:
- Minimum, maximum, and average RTT
- Packet loss rate


### Run Example
In two terminals:
```bash
# Terminal 1 (server)
python UDP_Pinger_Server.py


# Terminal 2 (client)
- Implement a GUI to visualize network metrics.