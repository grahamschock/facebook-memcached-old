import subprocess
import argparse
import time

cur_core = 0
nb_cores = 1
server = "10.10.1.2"
t = 1
k = 100
z = 135
d = 30

class client(object):
    def __init__(self, server_port, client_port, core):
        self.server_port = server_port
        self.client_port = client_port

        rate = ((client_port-11211)/10 + 1) * 100
        self.rate = rate

        self.args = ["taskset"]
        self.args.extend(["-c", str(core)])
        self.args.extend(["./mcblaster"])
        self.args.extend(["-k", str(k)])
        self.args.extend(["-t", str(t)])
        self.args.extend(["-z", str(z)])
        self.args.extend(["-u", str(server_port)])
        self.args.extend(["-f", str(client_port)])
        self.args.extend(["-r", str(rate)])
        self.args.extend(["-d", str(d)])
        self.args.extend(["{}".format(server)])

        self.log_file_path, log_file = self.create_log()
        print self.args
        
        self.p = subprocess.Popen(self.args, stdout=log_file)
        log_file.close()

    def stop(self):
        while self.process.poll() is None:
            time.sleep(1)
        self.log_file_path.close()

    def create_log(self):
        file_path = "logs/mcb_{}".format(self.client_port)
        f = open(file_path, "w+")
        f.write("ab arguments: {}\n\nSTDOUT:\n".format(str(self.args)))
        f.flush()
        return file_path, f

def increment_core_num(core):
    global cur_core
    p = core + cur_core
    cur_core = (cur_core + 1) % nb_cores
    return p

def start_clients(nb_nodes, server_port, client_port):
    client_list=[]
    for _ in range(nb_nodes):
        nc = increment_core_num(0)
        client_list.append(client(server_port, client_port, nc))

        if client_port > 0 and server_port > 0:
            client_port += 1
#            server_port += 1
    return client_list

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--nb_nodes", help="number of nodes", type=int)
    parser.add_argument("--nb_cores", help="number of cores", type=int)
    return parser.parse_args()

if __name__ == '__main__':

    args = parse_args()
    server = "10.10.1.2"
    nb_nodes = args.nb_nodes if args.nb_nodes else 1
    nb_cores = args.nb_cores if args.nb_cores else 4
    client_port = 11211
    server_port = 11311

    client_list = start_clients(nb_nodes, server_port, client_port)
