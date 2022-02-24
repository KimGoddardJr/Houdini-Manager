#!/usr/bin/env python

# runs every time a node gets created. use it to see the node path

# import hou
# from collections import OrderedDict


# """
# Linking this to the HSLU Houdini Tractor Manager Plugin.
# Its important to have this active in order to automatically delete
# the generated uuids on nodes that where droppped but have been duplicated.
# """


# def RemoveUUID(kwargs):
#     node = kwargs["node"]
#     userDataDict = node.userDataDict()
#     try:
#         if node.userData("uuid") != None:
#             print(userDataDict)
#             del userDataDict["uuid"]
#             userDataItemList = OrderedDict(userDataDict.items())
#             node.clearUserDataDict()

#             for name, prop in userDataItemList:
#                 node.setUserData(name, prop)

#     except KeyError as e:
#         print(e)
#         raise


# print("hellooooo")
# RemoveUUID(kwargs)
