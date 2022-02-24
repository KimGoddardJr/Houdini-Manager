import os


class PathMethods:
    @staticmethod
    def GetAbsPath():
        return os.path.dirname(os.path.abspath(__file__))

    @staticmethod
    def GetRealPath():
        return os.path.dirname(os.path.realpath(__file__))
