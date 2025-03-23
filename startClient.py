# import clientToolNoArduino as clientTool
import clientToolOriginalNoArduino as clientTool
import time


if __name__ == '__main__':
    while True:
        ip = input("[Enter address...]")
        if ip == ' ':
            break
        com = input("[Enter Arduino Mode...]")
        if com == ' ':
            break
        cli = clientTool.client(5, 5, ip, 9999, com)
        if cli.Disconnect or cli.Close:
            break
    print("[CLOSE]")
