#!/bin/bash

BUCKET_NAME="mibucketdevops1"
BACKUP_FILE="backup_$(date +%F).tar.gz"
LOG_FILE="backup.log"
DIRECTORIO="$HOME"

if ! command -v aws &> /dev/null; then
    echo "Error: AWS CLI no esta instalado." | tee -a $LOG_FILE
    exit 1
fi

if [ -z "$BUCKET_NAME" ]; then
    echo "Error: BUCKET_NAME no esta definido." | tee -a $LOG_FILE
    exit 1
fi

if [ ! -d "$DIRECTORIO" ]; then
    echo "Error: el directorio $DIRECTORIO no existe." | tee -a $LOG_FILE
    exit 1
fi

echo "Iniciando respaldo: $(date)" >> $LOG_FILE
tar -czf $BACKUP_FILE $DIRECTORIO >> $LOG_FILE 2>&1

if [ ! -f "$BACKUP_FILE" ]; then
    echo "Error: no se pudo crear el archivo de respaldo." | tee -a $LOG_FILE
    exit 1
fi

if aws s3 cp $BACKUP_FILE s3://$BUCKET_NAME/ >> $LOG_FILE 2>&1; then
    echo "Respaldo subido exitosamente." >> $LOG_FILE
else
    echo "Error en la subida del respaldo." | tee -a $LOG_FILE
    exit 1
fi

echo "Proceso finalizado: $(date)" >> $LOG_FILE
