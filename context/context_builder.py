import os

def context_builder(chunks , max_chars=3000):
    parts = []
    total = 0
    
    for c in chunks:
        content = ""
        original_content = c["content"]
        if isinstance(original_content, list):
            for item in original_content:
                content += f"\n{__join_object(item)}"
        elif isinstance(original_content, dict):
            content += __join_object(original_content)
        else:
            content = original_content

        block = f"[Fuente: {c["source"]}] {os.linesep}{content}\n"
        if total + len(block) > max_chars:
            break
        parts.append(block)
        total += len(block)

    return "\n".join(parts)

def __join_object(object):
    if isinstance(object,dict):
        content = os.linesep
        for key,val in object.items():
            val_content = __join_object(val)
            content += f"{key}: {val_content}{os.linesep}"
        return content
    return object
