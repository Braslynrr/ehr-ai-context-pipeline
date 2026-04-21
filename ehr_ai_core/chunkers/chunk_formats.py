from typing import get_origin, get_args

SCHEMAS = {
    "demographics": {
        "schema": {
            "name": str,
            "age": int,
            "gender": str,
            "blood_type": str
        },
        "prompt": 
        """{
            "name": string | null,
            "age": number | null,
            "gender": string | null,
            "blood_type": string | null
            }"""
    },

    "allergies": {
        "schema": list[str],
        "prompt": "list -> [ <string element> , ... ]"
    },

    "current_medications": {
        "schema": [{
            "dose": str,
            "name": str,
            "frequency": str
        }],
        "prompt": """
        [
        {
            "dose": string,
            "name": string,
            "frequency": string
        }
        ]
        """},
    "lab_result": {
        "schema": {
            "test": str,
            "results": dict[str,str]
        },
        "prompt": """
            {
            "test": string,
            "results": {
                "<metric>": "<value>"
            }
            }
            """
    },

    "recent_visit": {
        "schema": str,
        "prompt": """
        string
        """
    },
    "chronic_conditions": {
        "schema": list[str],
        "prompt": "[ <string element> , ... ]",
    },
    "intent": {
        "schema": {"language":str, "intent":str},
        "prompt": "{'intent': '<intent>', 'language': '<FullName Query language>'}"
    },
    "guide_modification": {
        "schema": {"entity":str,"action":str},
        "prompt": f"""{{ 
            "entity": "patient | chronic_conditions | allergies | recent_visit | demographics | current_medications | lab_results",
            "action": "create | update"
            }}"""
    }
}


def get_chunk_prompt(type: str):
    return SCHEMAS[type]["prompt"]

def get_chunk_schema(type: str):
    return SCHEMAS[type]["schema"]

def check_chunk_format(chunk: dict, type: str):
    schema = get_chunk_schema(type)

    missing = []

    for key in schema:
        
        origin_type = get_origin(key)
        arg_type = get_args(key)
        if origin_type == list:
            if not isinstance(chunk, list) or not all(isinstance(v, arg_type) for v in chunk):
                missing.append(key)
            continue

        if key not in chunk or chunk[key] is None:
            missing.append(key)

    return {
        "valid": len(missing) == 0,
        "missing": missing
    }