#!/bin/bash
export KUBECONFIG=~/.kube/config
kubectl exec -it $(kubectl get pods -l app=mysql -o jsonpath="{.items[0].metadata.name}") -- sh -c "mysqldump --defaults-extra-file=/var/lib/mysql/backup/mysqlpassword.cnf --host=localhost --user=root --port=3306  --databases datasaude > /var/lib/mysql/backup/backup-$(date +\%Y\%m\%d).sql"
find /mnt/volume/mysql_files/backup -name "*.sql" -type f -mtime +7 -delete
