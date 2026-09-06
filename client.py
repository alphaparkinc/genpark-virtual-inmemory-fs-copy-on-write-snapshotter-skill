import hashlib
import time
from typing import Dict, Any, List, Optional

class VirtualInMemoryFSSnapshotter:
    """
    Virtual in-memory filesystem with copy-on-write (COW) snapshots.
    Permits speculative execution by AI agents with atomic rollback to clean baseline state.
    """
    def __init__(self):
        self.files: Dict[str, bytes] = {}
        self.snapshots: Dict[str, Dict[str, bytes]] = {}

    def write_file(self, path: str, content: bytes) -> Dict[str, Any]:
        norm_path = "/" + path.strip().lstrip("/")
        self.files[norm_path] = content
        sha256 = hashlib.sha256(content).hexdigest()
        return {"path": norm_path, "bytes": len(content), "sha256": sha256}

    def read_file(self, path: str) -> Optional[bytes]:
        norm_path = "/" + path.strip().lstrip("/")
        return self.files.get(norm_path)

    def delete_file(self, path: str) -> bool:
        norm_path = "/" + path.strip().lstrip("/")
        if norm_path in self.files:
            del self.files[norm_path]
            return True
        return False

    def create_snapshot(self, snapshot_id: str) -> Dict[str, Any]:
        # Copy-on-write snapshot copy of dictionary references
        self.snapshots[snapshot_id] = dict(self.files)
        return {
            "snapshot_id": snapshot_id,
            "tracked_files_count": len(self.files),
            "timestamp": time.time()
        }

    def rollback_to_snapshot(self, snapshot_id: str) -> Dict[str, Any]:
        if snapshot_id not in self.snapshots:
            return {"status": "ERROR", "message": f"Snapshot {snapshot_id} does not exist."}
        
        self.files = dict(self.snapshots[snapshot_id])
        return {
            "status": "RESTORED",
            "snapshot_id": snapshot_id,
            "restored_files_count": len(self.files)
        }

    def list_files(self) -> List[str]:
        return sorted(list(self.files.keys()))
