from pulumi_aws.ec2 import GetAmiFilterArgs, Instance, SecurityGroup, get_ami
from utils.read_params import read_params


class AWS_EC2:
    def __init__(self):
        self.config = read_params()

    def get_ubuntu_ami(self):
        try:
            ubuntu = get_ami(
                most_recent=True,
                filters=[
                    GetAmiFilterArgs(
                        name="name",
                        values=[
                            "ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"
                        ],
                    ),
                    GetAmiFilterArgs(name="virtualization-type", values=["hvm"],),
                ],
                owners=["099720109477"],
            )

            return ubuntu

        except Exception as e:
            raise e

    def get_ec2_ingress_rule(self, instance_name):
        try:
            rule_lst = list(
                self.config["ec2_instances"][instance_name]["security_group"][
                    "ingress"
                ].values()
            )

            return rule_lst

        except Exception as e:
            raise e

    def get_ec2_security_group(self, instance_name, group_name):
        try:
            rule_lst = self.get_ec2_ingress_rule(instance_name)

            group = SecurityGroup(group_name, ingress=rule_lst)

            return group

        except Exception as e:
            raise e

    def get_ec2_instance(
        self, instance_tag_name, instance_type, instance_ami, security_group
    ):
        try:
            web = Instance(
                "web",
                ami=instance_ami.id,
                instance_type=instance_type,
                tags={"Name": instance_tag_name},
                vpc_security_group_ids=[security_group.id],
            )

        except Exception as e:
            raise e

    def deploy_ec2_instance(self, instance_name):
        try:
            ec2_config = self.config["ec2_instances"][instance_name]

            ec2_ami = self.get_ubuntu_ami()

            ec2_security_group = self.get_ec2_security_group(
                instance_name, ec2_config["sg_group"]
            )

            self.get_ec2_instance(
                ec2_config["tag_name"], ec2_config["type"], ec2_ami, ec2_security_group
            )

        except Exception as e:
            raise e
