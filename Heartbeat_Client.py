from socket import *
import time

class Heartbeat_Client:
    def __init__(self, server_ip, server_port):
        self.server_address = (server_ip, server_port)
        self.client_socket = socket(AF_INET, SOCK_DGRAM)
        self.client_socket.settimeout(1)  # Sets a timeout for receiving ACKs
        self.sequence_num = 0
        self.missed_acks = 0  # Counter for consecutive missed ACKs

    def send_heartbeat(self, interval):
        try:
            while True:
                self.sequence_num += 1
                send_time = time.time()
                buffer_size = 2048
                message = f"{self.sequence_num} {send_time}"
                self.client_socket.sendto(message.encode(), self.server_address)

                try:
                    response,_ = self.client_socket.recvfrom(buffer_size)
                    ack_time = time.time()
                    ack_status = response.decode()
                    self.print_current_statistics(ack_time, send_time, ack_status)
                    self.missed_acks = 1  # Reset missed ack counter on successful ack
                except timeout:
                    self.print_current_statistics(None, send_time, "No ACK Received")
                    self.missed_acks += 1

                if self.missed_acks >= 5:  # Assuming server is down after 5 missed ACKs
                    print("Server might be down, terminating heartbeat transmissions.")
                    break

                time.sleep(interval)
        except KeyboardInterrupt:
            print("Heartbeat sending terminated.")
        finally:
            self.client_socket.close()

    def print_current_statistics(self, ack_time, send_time, status):
        if ack_time:
            delay = ack_time - send_time
            print(f"Heartbeat #{self.sequence_num}: Sent at: {time.strftime('%H:%M:%S', time.localtime(send_time))}, "
                  f"ACK at: {time.strftime('%H:%M:%S', time.localtime(ack_time))}, "
                  f"Delay: {delay:.6f} sec, Status: {status}\n")
        else:
            print(f"Heartbeat #{self.sequence_num}: Sent at: {time.strftime('%H:%M:%S', time.localtime(send_time))}, "
                  f"ACK: None, Status: {status}\n")

if __name__ == '__main__':
    server_ip = gethostbyname(gethostname())  # automatically get the server IP address
    server_port = 12000
    interval = 1  # Interval in seconds between heartbeats
    heartbeat_client = Heartbeat_Client(server_ip, server_port)
    heartbeat_client.send_heartbeat(interval)
