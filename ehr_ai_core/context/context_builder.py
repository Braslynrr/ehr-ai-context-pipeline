from os import linesep
from typing import Iterable

def context_builder(chunks:Iterable[dict] , max_chars=3000):
    parts = []
    total = 0
    
    for c in chunks:
        content = ""
        original_content = c["content"]
        if isinstance(original_content, list):
            for item in original_content:
                content += f"{linesep}{join_object(item)}"
        elif isinstance(original_content, dict):
            content += join_object(original_content)
        else:
            content = original_content

        date_block =  f"- Date:{c.get('date', 'unknown')}{linesep}" if c.get("date", None) else ""

        block = f"{c['type']}: {linesep}{date_block}{content}{linesep}Source:{c['source']}{linesep}"
        if total + len(block) > max_chars:
            break
        parts.append(block)
        total += len(block)

    return f"{linesep}".join(parts)

def join_object(obj):
    if isinstance(obj,dict):
        content = f"{linesep}"
        for key,val in obj.items():
            val_content = join_object(val)
            content += f"-{key}: {val_content}{linesep}"
        return content
    elif isinstance(obj, list):
        return ", ".join(join_object(item) for item in obj)
    else:
        return str(obj)