import socket
from time import time, ctime

def main():
    # Set the server's address and port
    server_name = 'localhost'
    server_ip = socket.gethostbyname(server_name)
    server_port = 12000
    SERVER_ADDRESS = (server_name, server_port)

    # Create a UDP socket and set the timeout to 2 seconds
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(1)

    # Define the number of pings to send
    NUM_PINGS = 10

    # Initialize the minimum, maximum, and average RTTs, and the packet loss counter
    min_rtt = float('inf')
    max_rtt = float('-inf')
    total_rtt = 0
    packet_loss = 0
    buffer_size = 1024
    packets_recv = 0

    # Send pings to the server and process the responses
    for sequence_number in range(1, NUM_PINGS + 1):
        # Send the ping message
        message = f'Ping {sequence_number} successfully sent to {server_name} : {server_ip} \n({ctime()}) \n'.encode()
        send_time = time()
        client_socket.sendto(message, SERVER_ADDRESS)

        # Wait for a response or timeout
        try:
            response, SERVER_ADDRESS = client_socket.recvfrom(buffer_size)
            receive_time = time()
            rtt = (receive_time - send_time)
            rtt = round(rtt, 12) #Rounding off to nearest 12 decimal points
            total_rtt += rtt
            packets_recv += 1

            # Update the minimum, maximum, and average RTTs
            if rtt < min_rtt:
                min_rtt = rtt
            if rtt > max_rtt:
                max_rtt = rtt
            
            # Print the response message from the server
            print(f'Received: {response.decode()}')

        except socket.timeout:
            # Print "Request timed out"
            print(f'Request timed out \n')
            packet_loss += 1

    #Calculate the average RTTs
    avg_rtt = total_rtt / (NUM_PINGS - packet_loss)
    display(NUM_PINGS, packets_recv, min_rtt, max_rtt, avg_rtt, packet_loss)
    client_socket.close()
    

def display(NUM_PINGS, packets_recv, min_rtt, max_rtt, avg_rtt, packet_loss):
    packets_sent_message = f"Packets sent: {NUM_PINGS}"
    packets_recv_message = f"Packets received: {packets_recv}"

    print(packets_sent_message)
    print(packets_recv_message)

    # Calculate and print the packet loss rate (in percentage)
    packet_loss_percentage = packet_loss / NUM_PINGS * 100
    print(f'Packet loss rate: {packet_loss_percentage:.2f}%')

    # Calculate and print the minimum, maximum, and average RTTs
    print(f'Minimum RTT: {min_rtt:.12f}s') #12f to set the 12 decimal points
    print(f'Maximum RTT: {max_rtt:.12f}s')
    print(f'Average RTT: {avg_rtt:.12f}s')

main()
