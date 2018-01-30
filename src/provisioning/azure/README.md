# Provisioning on Azure

## Login / Setup

```bash
source aliases.sh

az login

az group create --name data_cleaning --location uksouth
```

## Create VM

```bash
az vm create --resource-group data_cleaning --name warehouse --image UbuntuLTS --generate-ssh-keys --admin-username azureuser --custom-data /root/cloud-init.txt
```

## Log into VM

```bash
azssh azureuser@<SERVER IP ADDRESS>
```

## Open port for Jupyter Notebook

```bash
az vm open-port --resource-group data_cleaning --name warehouse --port 8888
```

## Destroy VM

```bash
az vm delete --resource-group data_cleaning --name warehouse --yes
```