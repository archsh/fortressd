import sys

TEMPLATE = '''[program:ssh_%(loc)s_%(suffix)03d]
command=sshpass -p 'Aipu@admin#@!' ssh -N -L0.0.0.0:4%(loc)d%(suffix)03d:%(ip)s:%(port)d tvsee@localhost -p30022
autostart=true
autorestart=true
stdout_logfile=/var/log/supervisor/ssh_%(loc)s_%(suffix)03d_stdout.log       ; stdout log path, NONE for none; default AUTO
stdout_logfile_maxbytes=1MB   ; max # logfile bytes b4 rotation (default 50MB)
stdout_logfile_backups=10     ; # of stdout logfile backups (default 10)
stdout_capture_maxbytes=1MB   ; number of bytes in 'capturemode' (default 0)
stdout_events_enabled=false   ; emit events on stdout writes (default false)
stderr_logfile=/var/log/supervisor/ssh_%(loc)s_%(suffix)03d_stderr.log       ; stderr log path, NONE for none; default AUTO
stderr_logfile_maxbytes=1MB   ; max # logfile bytes b4 rotation (default 50MB)
stderr_logfile_backups=10     ; # of stderr logfile backups (default 10)
stderr_capture_maxbytes=1MB   ; number of bytes in 'capturemode' (default 0)
stderr_events_enabled=false   ; emit events on stderr writes (default false)
'''

CHENGDU_SERVERS = '''10.235.1.26
10.255.199.10
10.255.199.11
10.255.199.12
10.255.199.13
10.255.199.16
10.255.199.17
10.255.199.18
10.255.199.21
10.255.199.2
10.255.199.25
10.255.199.26
10.255.199.27
10.255.199.28
10.255.199.29
10.255.199.3
10.255.199.30
10.255.199.31
10.255.199.32
10.255.199.33
10.255.199.34
10.255.199.35
10.255.199.36
10.255.199.37
10.255.199.38
10.255.199.39
10.255.199.4
10.255.199.40
10.255.199.41
10.255.199.42
10.255.199.43
10.255.199.44
10.255.199.45
10.255.199.46
10.255.199.47
10.255.199.48
10.255.199.49
10.255.199.5
10.255.199.51
10.255.199.52
10.255.199.53
10.255.199.6
10.255.199.61
10.255.199.62
10.255.199.66
10.255.199.67
10.255.199.68
10.255.199.69
10.255.199.7
10.255.199.70
10.255.199.71
10.255.199.72
10.255.199.73
10.255.199.74
10.255.199.75
10.255.199.76
10.255.199.77
10.255.199.78
10.255.199.79
10.255.199.8
10.255.199.80
10.255.199.9
10.255.97.21
10.255.97.22
10.255.97.23
10.255.97.24
10.255.199.86
10.255.199.90
10.255.199.91
10.255.199.87
10.255.199.89
10.255.199.88
10.255.199.81
10.255.199.204
10.255.199.203
10.255.199.202
10.255.199.201'''

WUHAN_SERVERS = '''172.15.2.231
172.15.2.232
172.15.2.233
172.15.2.234
172.15.2.235
172.15.2.236
172.15.2.237
172.15.2.238
172.15.2.239
172.15.2.240
172.15.2.241
172.15.2.242
172.15.2.243
172.15.2.244
172.15.2.245
172.15.5.26'''

KUNMING_SERVERS = '''101.36.101.20
101.36.101.21
101.36.101.22
101.36.101.23
101.36.101.24
101.36.101.25
101.36.101.26
101.36.101.27
101.36.101.28
101.36.101.50
101.36.101.51
101.36.101.52
101.36.101.53
101.36.101.54
101.36.101.55
101.36.101.56
101.36.101.57
101.36.101.58
101.36.101.59'''

CHONGQING_SERVERS = '''101.36.99.124
101.36.99.125
101.36.99.126
101.36.99.127
101.36.99.128
101.36.99.129
101.36.99.131
101.36.99.132
101.36.99.133
101.36.99.134
101.36.99.135
101.36.99.136
101.36.99.137
101.36.99.138
101.36.99.140'''

GUIYANG_SERVERS = '''172.20.1.75
172.20.1.76
172.20.1.77
172.20.1.78
172.20.1.79'''

CHANGSHA_SERVERS = '''172.21.1.131
172.21.1.132
172.21.1.133
172.21.1.134
172.21.1.135'''

TEST_SERVERS = '''172.20.10.21
172.20.10.22'''

DATA_CENTERS = {
    "CHENGDU": {"id": 1, "list": CHENGDU_SERVERS.split("\n")},
    "WUHAN": {"id": 2, "list": WUHAN_SERVERS.split("\n")},
    "KUNMING": {"id": 3, "list": KUNMING_SERVERS.split("\n")},
    "CHONGQING": {"id": 4, "list": CHONGQING_SERVERS.split("\n")},
    "GUIYANG": {"id": 5, "list": GUIYANG_SERVERS.split("\n")},
    "CHANGSHA": {"id": 6, "list": CHANGSHA_SERVERS.split("\n")},
}

# DATA_CENTERS = { "TEST": {"id": 1, "list": TEST_SERVERS.split("\n")} }


def Generate_Server_Tunnel(loc_idx, server_ip, port):
    suffix = int(server_ip.split(".")[-1])
    return TEMPLATE % dict(loc=loc_idx, ip=server_ip, port=port, suffix=suffix)


if __name__ == '__main__':
    print("#####################################################################")
    print("####### Generated Supervisord App Configures by Python Script #######")
    print("#######         Mingcai SHEN <archsh@gmail.com>               #######")
    print("#######          Fri, Oct 07, 2016 10:02:05 AM                #######")
    print("#####################################################################")
    print("")
    # i = 1
    for k, vv in DATA_CENTERS.items():
        if sys.argv[1:] and k not in sys.argv[1:]:
            continue
        print("############################ Location: %d ############################" % vv.get("id"))
        print("### %s" % k)
        for svr in vv.get("list", []):
            ss = svr.split(":")
            if len(ss) > 1:
                ip = ss[0]
                port = int(ss[1])
            else:
                ip = ss[0]
                port = 30022
            print("## Server: %s " % svr)
            print(Generate_Server_Tunnel(vv.get("id"), ip, port))
            print("")
