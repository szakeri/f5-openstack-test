#!/bin/bash

# Make appropriate changes to tempest.conf
git clone https://bldr-git.int.lineratesystems.com/openstack/f5-os-testrunner-configs.git /root/f5-os-testrunner-configs
cp /root/f5-os-testrunner-configs/tempest/lbaasv2/tempest.conf.lbaasv2_agent_plugin /etc/tempest/tempest.conf
cp /root/f5-os-testrunner-configs/tempest/lbaasv2/accounts.yaml /etc/tempest/accounts.yaml
tempest="/etc/tempest/tempest.conf"

crudini --set $tempest network public_router_id $PUBLIC_ROUTER_ID
crudini --set $tempest network public_network_id $PUBLIC_NETWORK_ID
crudini --set $tempest identity uri $OS_AUTH_URL
crudini --set $tempest identity uri_v3 $OS_AUTH_URL_V3
crudini --set $tempest auth admin_tenant_id $OS_TENANT_ID
crudini --set $tempest f5_lbaasv2_driver icontrol_hostname $ICONTROL_IPADDR
crudini --set $tempest f5_lbaasv2_driver icontrol_username admin
crudini --set $tempest f5_lbaasv2_driver icontrol_password admin
crudini --set $tempest f5_lbaasv2_driver transport_url rabbit://guest:guest@$CONTROLLER_IPADDR:5672/
# Install the plugin by installing the f5lbaasv2driver
pip install /root/f5-openstack-lbaasv2-driver/
# Run tempest tests in workspace
tempest run --workspace tempest_test