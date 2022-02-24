#!/usr/bin/env python

# runs every time a node gets created. use it to see the node path

# import hou
# from collections import OrderedDict


# """
# Linking this to the HSLU Houdini Tractor Manager Plugin.
# Its important to have this active in order to automatically delete
# the generated uuids on nodes that where droppped but have been duplicated.
# """

# Thx Alex Rusev ---> https://forums.odforce.net/topic/30307-oncopy-event-in-hda/
# def is_copy_paste_event(kwargs):
#     if not kwargs["node"].name().startswith("original") and not kwargs[
#         "old_name"
#     ].startswith("original"):
#         original_node = (
#             kwargs["node"].parent().node("original0_of_%s" % kwargs["old_name"])
#         )
#         return True if original_node else False


# def RemoveUUID(kwargs):
#     node = kwargs["node"]
#     # userDataDict = node.userDataDict()
#     if is_copy_paste_event:
#         try:
#             if node.userData("uuid") != None:
#                 # print(userDataDict)
#                 # del userDataDict["uuid"]
#                 # userDataItemList = OrderedDict(userDataDict.items())
#                 node.clearUserDataDict()

#                 # for name, prop in userDataItemList:
#                 #     node.setUserData(name, prop)

#         except KeyError as e:
#             print(e)
#             raise


# print("hellooooo")
# RemoveUUID(kwargs)
