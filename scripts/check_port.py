#!/usr/bin/env python3
import socket
import sys
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    try:
        sock.bind(("0.0.0.0", args.port))
        print("free")
        sys.exit(0)
    except OSError:
        print(f"occupied")
        print(f"Port {args.port} is in use. Please stop the existing service or use a different port.")
        sys.exit(1)
    finally:
        sock.close()

if __name__ == "__main__":
    main()