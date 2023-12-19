import os

#LOG_FOLDER = "/var/log"
LOG_FOLDER = "logs"
DEFAULT_EVENT_COUNT = 1000

def get_log_events(filename, **kwargs):
    filepath = f"{LOG_FOLDER}/{filename}"
    file_size = os.stat(filepath).st_size
    chunk_size = min(int(400 * 1024), file_size)
    result = []
    n = DEFAULT_EVENT_COUNT

    if 'n' in kwargs:
        n = kwargs['n']

    def parse_lines(input, buffer):
        is_first = True
        last_index = len(input)
        index = input.rfind("\n")
        while index >= 0:
            if not is_first:
                result.append(input[index+1:last_index])
            else:
                result.append(input[index+1:last_index] + buffer)
                is_first = False
            
            last_index = index
            index = input.rfind("\n", 0, index)

        if last_index > 0:
            extra_buffer = (buffer if is_first else "")
            return input[0:last_index] + extra_buffer
        
        return ""

    pos = 0
    buffer = "" # holds content from previous read, in case we're in the middle of a line
    with open(filepath, "rb") as f:
        pos = f.seek(0, os.SEEK_END)
        while pos > 0 and len(result) < n:
            offset = min(chunk_size, pos)
            f.seek(pos)
            pos = f.seek(-1 * offset, os.SEEK_CUR)
            content = f.read(offset).decode("utf-8")
            buffer = parse_lines(content, buffer)

    if pos <= 0 and buffer:
        result.append(buffer)

    return result
