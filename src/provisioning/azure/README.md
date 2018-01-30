# Provisioning on Azure

Some notes and scripts on provisioning a reproducible demo VM for this project in the Azure cloud.

## Azure Login and Setup

```bash
source aliases.sh

az login

az group create --name data_cleaning --location uksouth
```

## Create VM

Take a note of the public IP address.

```bash
az vm create --resource-group data_cleaning --name warehouse --image UbuntuLTS --generate-ssh-keys --admin-username azureuser --custom-data /root/cloud-init.txt
```

## Log into VM

With the server IP address from above:

```bash
azssh azureuser@<SERVER IP ADDRESS>
```

## Expose ports for Jupyter Notebook & pgadmin

```bash
az vm open-port --resource-group data_cleaning --name warehouse --port 8888
az vm open-port --resource-group data_cleaning --name warehouse --port 5050 --priority 800
```

## Destroy VM

```bash
az vm delete --resource-group data_cleaning --name warehouse --yes
```