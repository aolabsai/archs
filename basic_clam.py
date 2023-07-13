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


description = "Basic Clam"
arch_i = [1, 1, 1]     # 3 neurons, 1 in each of 3 channels, corresponding to Food, Chemical-A, Chemical-B (present=1/not=0)
arch_z = [1]           # corresponding to Open=1/Close=0
arch_c = []            # 4 control neurons are included in the default first channel-- 0-label, 1-force_positive, 2-force_negative, 3-default pleasure instinct triggered when I__flat[0]=1 and Z of previous step Z__flat[0]=1
connector_function = "full_conn"