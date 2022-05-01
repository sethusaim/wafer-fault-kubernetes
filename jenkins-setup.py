from json import loads
from subprocess import PIPE, Popen, run

cluster_name = "wafer-test-1"

def run_command(cmd):
    try:
        run(cmd)

    except Exception as e:
        raise e


def get_command_output(cmd):
    try:
        result = Popen(cmd, stdout=PIPE).stdout.read().decode()

        return result

    except Exception as e:
        raise e


vpc_id = get_command_output(
    'aws eks describe-cluster --name getting-started-eks --query "cluster.resourcesVpcConfig.vpcId" --output text'
)

cidr_block = get_command_output(
    'aws ec2 describe-vpcs --vpc-ids vpc-id --query "Vpcs[].CidrBlock" --output text'
)

sg_group_str = get_command_output(
    f"aws ec2 create-security-group --description efs-test-sg --group-name efs-sg --vpc-id {vpc_id}"
)

sg_group_dic = loads(sg_group_str)

sg_group = sg_group_dic["GroupId"]

run_command(
    f"aws ec2 authorize-security-group-ingress --group-id {sg_group}  --protocol tcp --port 2049 --cidr {cidr_block}"
)

efs_str = get_command_output("aws efs create-file-system --creation-token eks-efs")

efs_dic = loads(efs_str)

file_sys_id = efs_dic["FileSystemId"]

subnet_id = get_command_output(
    f"aws ec2 describe-instances --filters Name=vpc-id,Values={vpc_id} --query 'Reservation[*].Instances[].SubnetId'"
)

run_command(
    f"aws efs create-mount-target --file-system-id {file_sys_id} --subnet-id {subnet_id} --security-group {sg_group}"
)

# efs_access_point = get_command_output(f'aws efs create-access-point --file-system-id {file_sys_id} --posix-user Uid=1000,Gid=1000 --root-directory')

run_command("kubectl create ns jenkins")

run_command(
    "wget 'https://raw.githubusercontent.com/marcel-dempers/docker-development-youtube-series/master/jenkins/amazon-eks/jenkins.pv.yaml'"
)

run_command(f"sed -i 's+volumeHandle.*+volumeHandle: {file_sys_id}+g' jenkins.pv.yaml")

run_command(
    "wget 'https://raw.githubusercontent.com/marcel-dempers/docker-development-youtube-series/master/jenkins/amazon-eks/jenkins.pvc.yaml'"
)

run_command("kubectl apply -n jenkins -f jenkins.pvc.yaml")

run_command(
    "wget https://raw.githubusercontent.com/marcel-dempers/docker-development-youtube-series/master/jenkins/jenkins.rbac.yaml"
)

run_command(
    "wget https://raw.githubusercontent.com/marcel-dempers/docker-development-youtube-series/master/jenkins/jenkins.deployment.yaml"
)

run_command("kubectl apply -n jenkins -f jenkins.rbac.yaml")

run_command("kubectl apply -n jenkins -f jenkins.deployment.yaml")

run_command(
    "wget https://raw.githubusercontent.com/marcel-dempers/docker-development-youtube-series/master/jenkins/jenkins.service.yaml"
)

run_command("kubectl apply -n jenkins -f jenkins.service.yaml")
