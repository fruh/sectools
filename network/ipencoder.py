#!/ust/bin/python
import sys


encodings_dots = ("%02x", "%04o", "%d")
encodings = ("0x%x", "0%o", "%d")


def join_dots(s, length=4):
    ret = ""

    for i in range(length - 1):
        ret += s + "."
    ret += s
    return ret


def ip_fuzz_dots(ip, encodings):
    ip_dec = tuple(map(int, ip.split('.')))

    for e in encodings:
        format_string = join_dots(e)
        print(format_string % ip_dec)


def ip_fuzz(ip, encodings):
    ip_dec = tuple(map(int, ip.split('.')))
    ip_dec = ip_dec[0] * 256**3 + ip_dec[1] * 256**2 + ip_dec[2] * 256 + ip_dec[3]

    for e in encodings:
        print(e % ip_dec)


if __name__ == "__main__":
    ip = sys.argv[1]
    ip_fuzz_dots(ip, encodings_dots)
    ip_fuzz(ip, encodings)
