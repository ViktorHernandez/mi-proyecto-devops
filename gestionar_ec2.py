import boto3
from botocore.exceptions import BotoCoreError, ClientError

ec2 = boto3.client('ec2', region_name='us-east-2')

def listar_instancias():
    try:
        response = ec2.describe_instances()
        instancias = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                iid = instance['InstanceId']
                estado = instance['State']['Name']
                instancias.append(iid)
                print(f'ID: {iid}, Estado: {estado}')
        if not instancias:
            print('No se encontraron instancias en la region.')
        return instancias
    except ClientError as e:
        print(f'Error de AWS: {e.response["Error"]["Message"]}')
        return []
    except BotoCoreError as e:
        print(f'Error de conexion: {e}')
        return []

def gestionar_instancia(instancia_id, accion):
    if not instancia_id or instancia_id == 'ID_INSTANCIA':
        print('Error: ID de instancia no valido.')
        return
    if accion not in ['iniciar', 'detener']:
        print('Error: accion no valida. Usa iniciar o detener.')
        return
    try:
        response = ec2.describe_instances(InstanceIds=[instancia_id])
        estado = response['Reservations'][0]['Instances'][0]['State']['Name']
        if accion == 'iniciar' and estado == 'stopped':
            ec2.start_instances(InstanceIds=[instancia_id])
            print(f'Instancia {instancia_id} iniciada.')
        elif accion == 'detener' and estado == 'running':
            ec2.stop_instances(InstanceIds=[instancia_id])
            print(f'Instancia {instancia_id} detenida.')
        else:
            print(f'Instancia {instancia_id} ya esta en estado {estado}. No se realizo ninguna accion.')
    except ClientError as e:
        print(f'Error de AWS: {e.response["Error"]["Message"]}')
    except BotoCoreError as e:
        print(f'Error de conexion: {e}')

print('--- Listando instancias ---')
listar_instancias()
print('--- Gestionando instancia ---')
gestionar_instancia('i-017f662f6577a960a', 'iniciar')