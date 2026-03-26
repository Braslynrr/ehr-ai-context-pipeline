from os import linesep

def context_builder(chunks , max_chars=3000):
    parts = []
    total = 0
    
    for c in chunks:
        content = ""
        original_content = c["content"]
        if isinstance(original_content, list):
            for item in original_content:
                content += f"{linesep}{__join_object(item)}"
        elif isinstance(original_content, dict):
            content += __join_object(original_content)
        else:
            content = original_content

        block = f"[type: {c['type']}, source: {c['source']}] {linesep}{content}{linesep}"
        if total + len(block) > max_chars:
            break
        parts.append(block)
        total += len(block)

    return f"{linesep}".join(parts)

def __join_object(obj):
    if isinstance(obj,dict):
        content = f"{linesep}"
        for key,val in obj.items():
            val_content = __join_object(val)
            content += f"{key}: {val_content}{linesep}"
        return content
    elif isinstance(obj, list):
        return ", ".join(__join_object(item) for item in obj)
    else:
        return str(obj)