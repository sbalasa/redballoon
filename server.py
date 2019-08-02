import sys
import time
import click
import socket
import logging
import traceback


# Logger for Verification failures
logger_verification = logging.getLogger(__name__+"verification")
verification_handler = logging.FileHandler("verification_failures.log")
logger_verification.addHandler(verification_handler)
logger_verification.setLevel(logging.INFO)

# Logger for Checksum failures
logger_checksum = logging.getLogger(__name__+"checksum")
checksum_handler = logging.FileHandler("checksum_failures.log")
logger_checksum.addHandler(checksum_handler)
logger_checksum.setLevel(logging.INFO)


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDP_IP = "127.0.0.1"


def write_log(log_type, msg, delay):
    time.sleep(delay)
    if log_type == "verification":
        logger_verification.info(msg)
    else:
        logger_checksum.info(msg)


@click.command()
@click.option("-p", default='1337', help="Port to listen UDP packets from")
@click.option("-d", default='1', help="Delay in seconds for writing to log files")
@click.option("--binaries", default='{"0x42": "cat.jpg"}', help="Dictionary of {packet_id: binary_path} mappings")
@click.option("--keys", default='{"0x42": "key.bin"}', help="Dictionary of {packet_id: key_file_path} mappings")
def main(p, d, binaries, keys):
    sock.bind((UDP_IP, int(p)))
    while True:
        data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
        print "----------------START----------------------"
        print "received message:", data
        print "----------------END-----------------------\n"


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Processor exit with: {}".format(e))
        traceback.print_exc()
        sys.exit(1)  # exit with error
