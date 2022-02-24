#!/usr/bin/env python

# runs every time a node gets loaded. If executed after file is loaded,
# nodes will perform certain tasks on duplication

import hou
from collections import OrderedDict

"""
Linking this to the HSLU Houdini Tractor Manager Plugin.
Its important to have this active in order to automatically delete
the generated uuids on nodes that where droppped but have been duplicated.
"""


def RemoveUUID(kwargs):
    node = kwargs["node"]
    try:
        if node.userData("uuid") != None:
            print(node.userDataDict())
            node.clearUserDataDict()

    except KeyError as e:
        print(e)
        raise


if hou.hipFile.isLoadingHipFile():
    print("Loading")
else:
    print("copying")
    RemoveUUID(kwargs)
