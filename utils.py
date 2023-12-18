import os

#LOG_FOLDER = "/var/log"
LOG_FOLDER = "logs"

def get_log_events(filename):
    filepath = f"{LOG_FOLDER}/{filename}"
    file_size = os.stat(filepath).st_size
    chunk_size = min(int(400 * 1024), file_size)

    result = []
    n = 1000
    pos = 0
    with open(filepath, "rb") as f:
        pos = f.seek(0, os.SEEK_END)
        while pos > 0: # and len(result) < n:
            offset = min(chunk_size, pos)
            f.seek(pos)
            pos = f.seek(-1 * offset, os.SEEK_CUR)
            content = f.read(offset).decode("utf-8")

            # TODO: actually figure out the lines
            result.append(content)

    return result
