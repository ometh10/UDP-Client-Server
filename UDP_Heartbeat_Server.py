from socket import *
import time

class Heartbeat_Server:
    def __init__(self, server_ip, server_port):
        self.server_socket = socket(AF_INET, SOCK_DGRAM)
        self.server_socket.bind((server_ip, server_port))
        self.server_socket.settimeout(1)  # Setting reasonable timeout for receiving
        
        print(f"Heartbeat server is running on {server_ip}: {server_port}\n")

    def receive_heartbeats(self):
        buffer_size = 2048
        expected_interval = 1  # Interval in seconds that the server expects heartbeats
        last_received_time = time.time()

        while True:
            try:
                client_message, client_address = self.server_socket.recvfrom(buffer_size)
                recv_time = time.time()
                sequence_num, client_time = client_message.decode().split()
                sequence_num = int(sequence_num)
                client_time = float(client_time)

                time_diff = recv_time - client_time

                if time_diff > 0.0005:
                    self.heartbeat_missing(client_address, sequence_num, time_diff)
                else:
                    self.client_ack(client_address, sequence_num, time_diff, client_time)
                last_received_time = time.time()  # Update the last received time
                
            except timeout:
                current_time = time.time()
                time_since_last_received = current_time - last_received_time
                if time_since_last_received > expected_interval:
                    self.report_lost_heartbeat(time_since_last_received)
                    
                last_received_time = current_time  # Reset last received time after reporting


    def report_lost_heartbeat(self, time_since_last_received):
        print(f"Heartbeat lost!!! : no heartbeat received for {time_since_last_received:.6f} seconds, Time Stamp: {time.ctime()}")

    def heartbeat_missing(self, client_address, sequence_num, time_diff):
        missing_response = f"Delayed HeartBeat: SEQUENCE NO = #{sequence_num}, Time difference: {time_diff:.6f}, Time Stamp: {time.time()}"
        print(missing_response)
        self.server_socket.sendto("Acknowledgment - Missing heartbeat detected!!!".encode(), client_address)

    def client_ack(self, client_address, sequence_num, time_diff, client_time):
        client_time_str = time.strftime('%H:%M:%S', time.localtime(client_time))
        confirm_msg = f"HeartBeat received: {client_address[0]}:{client_address[1]}, SEQUENCE NO = #{sequence_num}, Send Time: {client_time_str}, Time difference: {time_diff:.6f}"
        print(confirm_msg)
        self.server_socket.sendto("Acknowledgment - Success!".encode(), client_address)

if __name__ == '__main__':
    server_ip = gethostbyname(gethostname())
    server_port = 12000
    heartbeat_server = Heartbeat_Server(server_ip, server_port)
    heartbeat_server.receive_heartbeats()
    
