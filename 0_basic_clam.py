# -*- coding: utf-8 -*-
"""
// aolabs.ai software >ao_core/Arch.py (C) 2023 Animo Omnis Corporation. All Rights Reserved.

Thank you for your curiosity!
"""


## // Basic Clam -- Reference Design #0
# 
# Our simplest Agent, our 'hello, world.'
#
# For interactive visual representation of this Arch:
#    https://miro.com/app/board/uXjVM_kESvI=/?share_link_id=72701488535
#
# Cutomize and upload this Arch to our API to create Agents: https://docs.aolabs.ai/reference/kennelcreate
#


description = "Basic Clam"
arch_i = [1, 1, 1]     # 3 neurons, 1 in each of 3 channels, corresponding to Food, Chemical-A, Chemical-B (present=1/not=0)
arch_z = [1]           # corresponding to Open=1/Close=0
arch_c = []            # 4 control neurons are included in the default first channel-- 0-label, 1-force_positive, 2-force_negative, 3-default pleasure instinct triggered when I__flat[0]=1 and Z of previous step Z__flat[0]=1
connector_function = "full_conn"

# To maintain compatability with our API, do not change the variable name "Arch" or the constructor class "ao.Arch" in the line below (the API is pre-loaded with a version of the Arch class in this repo's main branch, hence "ao.Arch")
Arch = ao.Arch(arch_i, arch_z, arch_c, connector_function, description)