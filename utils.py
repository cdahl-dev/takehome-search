import os

#LOG_FOLDER = "/var/log"
LOG_FOLDER = "logs"
DEFAULT_EVENT_COUNT = 1000

def get_log_events(filename, **kwargs):
    filepath = f"{LOG_FOLDER}/{filename}"
    file_size = os.stat(filepath).st_size
    chunk_size = min(int(2000 * 1024), file_size)
    
    result = []
    n = DEFAULT_EVENT_COUNT
    keyword = "" # support only one for now

    if 'n' in kwargs:
        n = kwargs['n']

    if 'keyword' in kwargs:
        keyword = kwargs['keyword']

    def has_match(input):
        return not keyword or keyword in input

    def process_line(line):
        if has_match(line):
            result.append(line)

    def parse_lines(input, buffer):
        is_first = True
        last_index = len(input)
        input_match = has_match(input)
        index = input.rfind("\n")
 
        # edge case: a match for the keyword could be broken up across chunks
        if not input_match and buffer:
            input_match = index >= 0 and has_match(input[index+1:last_index] + buffer)

        if input_match:
            while index >= 0 and len(result) < n:
                line = input[index+1:last_index]
                if not is_first:
                    process_line(line)
                else:
                    process_line(line + buffer)
                    is_first = False
                
                last_index = index
                index = input.rfind("\n", 0, index)
        else:
            # no match, but we still may have buffer content
            last_index = input.find("\n")
            if last_index < 0:
                last_index = len(input)

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

    if pos <= 0 and buffer and len(result) < n:
        process_line(buffer)

    return result
