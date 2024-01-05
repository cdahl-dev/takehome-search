import os
import re
from app.settings import Settings

def get_log_events(filename, **kwargs):    
    filepath = f"{Settings.LOG_FOLDER}/{filename}"
    file_size = os.stat(filepath).st_size
    chunk_size = min(Settings.CHUNK_SIZE, file_size)
    
    result = []
    n = Settings.DEFAULT_EVENT_COUNT
    keywords = []
    keyword_pattern = None

    if 'n' in kwargs:
        n = kwargs['n']

    if 'keywords' in kwargs:
        keywords = kwargs['keywords'].lower().split()
        if keywords:
            keyword_pattern = re.compile('(?=.*' + ')(?=.*'.join(keywords) + ')', re.IGNORECASE | re.DOTALL)

    def has_match(input):
        #input_lower = input.lower()
        if (not keyword_pattern) or keyword_pattern.match(input):
            return True
        
        return False
    
    def process_line(line):
        if has_match(line):
            result.append(line)

    def parse_lines(input, buffer):
        # append the buffer from last time to the input
        full_input = input + buffer
        last_index = len(full_input)
        index = full_input.rfind("\n")

        if has_match(full_input):
            while index >= 0 and len(result) < n:
                line = full_input[index+1:last_index]
                process_line(line)
                
                last_index = index
                index = full_input.rfind("\n", 0, index)
        else:
            # no match, but we still may have buffer content
            last_index = full_input.find("\n")
            if last_index < 0:
                last_index = len(full_input)

        if last_index > 0:
            return full_input[0:last_index]
        
        return ""

    pos = 0
    buffer = "" # holds content from previous read, in case we're in the middle of a line
    with open(filepath, "rb") as f:
        pos = f.seek(0, os.SEEK_END)
        while pos > 0 and len(result) < n:
            offset = min(chunk_size, pos)
            f.seek(pos)
            pos = f.seek(-1 * offset, os.SEEK_CUR)
            # Note: assumes all files are utf-8 for now - should probably detect file encoding
            content = f.read(offset).decode("utf-8")
            buffer = parse_lines(content, buffer)

    if pos <= 0 and buffer and len(result) < n:
        process_line(buffer)

    return result
