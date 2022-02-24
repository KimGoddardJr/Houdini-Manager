"""
A simple script to kick off a certain ROP remotely, optionally
with a given framerange.
Usage: hython path/to/script/houBatch.py /path/to/hipfile /hou/path/to/rop
TODO: Add options for multiple ROPs, hperf.
"""
import hou, sys, os
hou.putenv("HOUDINI_PATH", "{}{}".format(os.environ["HOUDINI_PATH"][0:-1], ":&") )
hou.putenv("HOUDINI", os.environ["HOUDINI"])
hou.putenv("HOUDINI_OTLSCAN_PATH", "{}{}".format(os.environ["HOUDINI_OTLSCAN_PATH"][0:-2], ":&"))

#for k, v in os.environ.items():
#    print k, v

print(sys.argv[1])

# Load the hip file
hou.hipFile.load(sys.argv[1])

# If framerange option, set it
#if sys.argv[3]:
#    hou.parmTuple( "%s/f" %(sys.argv[2]) ).set((sys.argv[3],sys.argv[4],1.0))

# Start the render
n = hou.node(sys.argv[2])
n.setParms({"f1":sys.argv[3]})
n.setParms({"f2":sys.argv[4]})
n.setParms({"f3":sys.argv[5]})
n.render()

# When finished, exit
sys.exit(0)