import boto3
import subprocess
import os

def ec2():

    ec2 = boto3.client('ec2')

    while True:
        response = ec2.describe_instances()
        instances = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instances.append(instance)

        print("\nAvailable EC2 instances:")
        for i, instance in enumerate(instances):
            name_tag = next((tag['Value'] for tag in instance.get('Tags', []) if tag['Key'] == 'Name'), "No Name")
            print(f"{i+1}. {instance['InstanceId']} ({name_tag})")
        print("0. Exit")

        selection = input("\nEnter the number of the instance you want to connect to (0 to exit): ")
        if selection == '0':
            break
        instance_id = instances[int(selection)-1]['InstanceId']
        instance_type = instances[int(selection)-1]['PlatformDetails']
    
        print(f"\nConnecting to instance {instance_id}...")
    
        if instance_type == 'Windows': 
            port_number = '3389'
        else:
            port_number = '22'
    
        command = f"aws ssm start-session --target {instance_id} --document-name AWS-StartPortForwardingSession --parameters 'localPortNumber=9001,portNumber={port_number}'"
        print (command)

        os.system(command)

if __name__ == "__main__":
    ec2()