## // Netbox- Device Discovery -- Reference Design #2
# Source: https://github.com/aolabsai/archs/blob/main/2_netbox-device_discovery.py
# 
# For interactive visual representation of this Arch:
#    https://miro.com/app/live-embed/uXjVM_kESvI=/?moveToViewport=139623,-44894,15015,11297&embedId=159693252308

description = "Trial run- similar to netbox"
arch_i = [15, 15, 15]               # a scaled up Basic Clam, with 3 input channels with 10 neurons each, corresponding to device Mfg, Type, and Site (from IDss to 10-digit binary)
arch_z = [15]                       # 10 neurons in 1 channel to encode device Role IDs
arch_c = []
connector_function = "rand_conn"
# device mfg, type, and site are stored as strings (names) with associated unique IDs
# using 10 binary neurons to encode integer IDs means we can encode up to 2^10 = 1048 unique binary values.


# To maintain compatability with our API, do not change the variable name "Arch" or the constructor class "ao.Arch" in the line below (the API is pre-loaded with a version of the Arch class in this repo's main branch, hence "ao.Arch")
Arch = arc.Arch(arch_i, arch_z, arch_c, connector_function, description)
