#!/usr/bin/env python

import hou
#hou.ui.displayMessage(repr(kwargs))
node = kwargs['node']
node.setParms({'tractor_hostname':'10.180.128.5', 'tractor_port':8080, 'tractor_user': 'root' })