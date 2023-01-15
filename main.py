import uvicorn
from uvicorn.supervisors.watchgodreload import CustomWatcher


_ignored = {
    "models",
}


class _WatchgodWatcher(CustomWatcher):
    def __init__(self, *args, **kwargs):
        self.ignored_dirs.update(_ignored)
        super(_WatchgodWatcher, self).__init__(*args, **kwargs)


uvicorn.supervisors.watchgodreload.CustomWatcher = _WatchgodWatcher

if __name__ == "__main__":
    uvicorn.run("generator.app:api", host="127.0.0.1", port=8000, log_level="info")