#!/usrb/bin/python
import itertools

allowed = ["localhost"]
schemes = ["http", "https"]
hostlist = ["first.p.batata.sk", "second.p.batata.sk", "third.p.batata.sk"] + allowed
ports = ["80", "443"]

first = "first.p.batata.sk"
second = "second.p.batata.sk"
third = "third.p.batata.sk"

fuzz_list = [
    "{scheme}://{h1} &@{h2}# @{h3}/",
    "{scheme}://{h1}:{port1}:{port2}/",
    "{scheme}://{h1}#@{h2}/",
    "{scheme}://foo@{h1}:{port1}@{h2}/",
    "{scheme}://foo@{h1} @{h2}/",
    "{scheme}://{h1}\\t{h2}/",
    "{scheme}://{h1}%09{h2}/",
    "{scheme}://{h1}%2509{h2}/",
    "{scheme}://0/",
    "{scheme}://{h1}/"
]

if __name__ == "__main__":
    fuzzed = set()

    for i in itertools.product(schemes, hostlist, hostlist, hostlist, ports, ports):
        if i[1] == i[2] or i[4] == i[5]:
            continue
        for u in fuzz_list:
            fuzzed.add(u.format(scheme=i[0], h1=i[1], h2=i[2], h3=i[3], port1=i[4], port2=i[5]))

    for f in fuzzed:
        print(f)