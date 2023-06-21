# -*- coding: utf-8 -*-
"""
Created on Sat Mar  4 21:32:52 2023

@author: alebr
"""

#%%

def deviceToIO(d):
    info = {
        'id': d.id,
        'idBin': format(d.id, '010b'),
        'type': d.device_type.id,
        'typeBin': format(d.device_type, '010b'),
        'manufacturer': d.device_type.manufacturer.id,
        'manufacturerBin': format(d.device_type.manufacturer.id, '010b'),
        'site': d.site.id,
        'siteBin': format(d.site.id, '010b'),
        'role': d.device_role.id,
        'roleBin': format(d.device_role.id, '010b'),
    }
    return info



#%%
import pynetbox
nb = pynetbox.api(
    'https://demo.netbox.dev',
    token='047effeb2d662dd6fb42f7a7bc279f567be4ac11',
    threading=True,
)
devices = nb.dcim.devices.all()

# arraySize = 10

# # map binary strings to ids
# roles = {}
# manufacturers = {}
# sites = {}
# types = {}

# roles_id_to_str = {}

# devices_array = np.zeros(400, dtype='O')
# devices_array_IO = np.copy(devices_array)
# devices_names = np.copy(devices_array)

# inc = 0
# #populate devices array
# for device in devices:

#     devices_names[inc] = str(device)
#     devices_array_IO[inc] = deviceToIO(device, arraySize)

#     #add device data to sets so they can be options in text boxes
#     roles[str(device.device_role)] = device.device_role.id
#     manufacturers[str(device.device_type.manufacturer)] = device.device_type.manufacturer.id
#     sites[str(device.site)] = device.site.id
#     types[str(device.device_type)] = device.device_type.id

#     roles_id_to_str[device.device_role.id] = str(device.device_role)    

#     # count number of devices
#     inc += 1

# devices_array_IO = devices_array_IO[0:inc]
# devices_names = devices_names[0:inc]

# num_test_devices = 10

# test_devices = np.random.choice(inc, num_test_devices, replace=False)    

# train_devices_array_IO = np.delete(devices_array_IO, test_devices)
# test_devices_array_IO = devices_array_IO[test_devices]

# test_devices_names = devices_names[test_devices]

# nbd = {
# "roles": roles,
# "manufacturers" : manufacturers,
# "sites" : sites,
# "types" : types,
# "roles_id_to_str" : roles_id_to_str,
# "inc" : inc,
# "test_devices_names" : test_devices_names,
# "devices_array_IO" : train_devices_array_IO
# }