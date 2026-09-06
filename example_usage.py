import json
from client import VirtualInMemoryFSSnapshotter

def main():
    vfs = VirtualInMemoryFFS = VirtualInMemoryFSSnapshotter()
    vfs.write_file("/src/app.py", b"print('version 1.0')")
    snap_res = vfs.create_snapshot("clean_checkpoint_1")
    print("Snapshot Created:", json.dumps(snap_res, indent=2))
    
    # Speculative mutation
    vfs.write_file("/src/app.py", b"print('destructive speculative edit')")
    vfs.write_file("/tmp/junk.log", b"debug crash logs")
    assert b"destructive" in vfs.read_file("/src/app.py")
    
    # Atomic rollback
    rollback_res = vfs.rollback_to_snapshot("clean_checkpoint_1")
    print("Rollback Result:", json.dumps(rollback_res, indent=2))
    assert vfs.read_file("/src/app.py") == b"print('version 1.0')"
    assert vfs.read_file("/tmp/junk.log") is None
    print("Virtual in-memory filesystem verification: PASS")

if __name__ == "__main__":
    main()
