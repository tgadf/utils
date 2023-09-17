from utils import FileInfo
from utils import DirInfo
from os import getcwd


def test_fileinfo():
    path = getcwd()
    dinfo = DirInfo(path)
    finfo = dinfo.join("dummy.x")

    finfo2 = FileInfo("dummy.x")
    assert finfo.name == finfo2.name, f"FileInfo names are not equal!"

    finfo.touch(debug=False)
    assert finfo.exists(), f"Could not create [{finfo}]"
    finfo.rmFile(debug=False)

def test_dirinfo():
    path = getcwd()
    dinfo = DirInfo(path)
    
    path2 = getcwd()
    dinfo2 = DirInfo(path2)
    assert dinfo == dinfo2, f"DirInfo __eq__ is not working correctly: {dinfo} vs {dinfo2}"

    newdinfo = dinfo.join("test_dirinfo")
    newdinfo.mkDir(debug=False)
    assert newdinfo.exists(), f"Could not create [{newdinfo}]"
    newdinfo.rmDir(debug=False)

