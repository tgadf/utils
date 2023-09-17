from utils import RecentFiles
from utils import DirInfo
from os import getcwd


def test_recentfiles():
    dinfo = DirInfo(getcwd())
    files = dinfo.getFiles()
    assert len(files) > 0, f"nFiles = {len(files)}"
    
    rf = RecentFiles(files=files, verbose=False)
    retval = rf.getFilesByRecency(expr='> 0 Days')
    assert len(retval) == len(files), f"Time error with {rf}"

    rf = RecentFiles(files=files, verbose=False)
    retval = rf.getFilesByRecency(expr=None)
    assert len(retval) == len(files), f"Time error with {rf}"
    
    rf = RecentFiles(files=files, verbose=False)
    retval = rf.getFilesByRecency(expr='< 0 Days')
    assert len(retval) < len(files), f"Time error with {rf}"


if __name__ == "__main__":
    test_recentfiles()