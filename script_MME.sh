#!/bin/bash

# Define variables
REMOTE_USER="********"
REMOTE_HOST="10.47.23.6"
REMOTE_PASS="**********" 
ARCHIVO_RESULTADO="/home/oem/resultado_MME_VF.txt"
COMANDOS=$(cat <<'EOF'
echo -n "alarmas_" && echo "inicio"&& gsh show_fm_alarm | awk '{print $1 " " $2 " " $3 " " $5 }'  && echo -n "alarmas_" && echo "fin"
echo -n "eventos_" && echo "inicio"&& gsh list_events |awk '{print $1}'| sort | uniq -c && echo -n "eventos_" && echo "fin"
echo -n "enodeb_" && echo "inicio"&& gsh show_mme_global_enodeb -ens disconnected && echo -n "enodeb_" && echo "fin"
echo -n "diameter_" && echo "inicio"&& gsh list_diameter_peer -sip '' -status '' -pn '' -rhn '' && echo -n "diameter_" && echo "fin"
echo -n "CPU_" && echo "inicio"&& gsh get_eq_cpu_load && echo -n "CPU_" && echo "fin"
echo -n "HW_" && echo "inicio"&& hw_status| awk '{print $1 " " $2 " " $3 " " $4 " "$5 " " $6 " " $7 " "$8  }' && echo -n "HW_" && echo "fin"
echo -n "ip_" && echo "inicio"&& getAll_ip_if && echo -n "ip_" && echo "fin"
echo -n "kpi_" && echo "inicio"&& pdc_kpi.pl -n 60 -i 60 && echo -n "kpi_" && echo "fin"
exit
EOF
)

rm -rf $ARCHIVO_RESULTADO
sshpass -p $REMOTE_PASS ssh -o StrictHostKeyChecking=no $REMOTE_USER@$REMOTE_HOST eval "$COMANDOS" >> $ARCHIVO_RESULTADO
