import paramiko
import scp

def send_json(local_path, remote_path, hostname, user):
    with paramiko.SSHClient() as ssh:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.load_system_host_keys()
        ssh.connect(
            hostname,
            username=user
        )

        with scp.SCPClient(ssh.get_transport()) as s:
            s.put(
                remote_path=remote_path,
                files=local_path
            )


def run_cmd(hostname, user, cmd):
    with paramiko.SSHClient() as ssh:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.load_system_host_keys()
        ssh.connect(
            hostname,
            username=user
        )
        
        stdin, stdout, stderr = ssh.exec_command(cmd)
        print(stdout)
        print(stdin)


if __name__ == "__main__":
    send_json(
        local_path="/workspace/ci-server/dump/2023-1125-162411.json",
        remote_path="/tmp",
        hostname="",
        user=""
    )