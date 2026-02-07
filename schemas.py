pet = {
    "type": "object",
    "required": ["name"],
    "properties": {
        "id": {
            "type": "integer"
        },
        "name": {
            "type": "string"
        },
        "type": {
            "type": "string",
            "enum": ["cat", "dog", "fish"]
        },
        "status": {
            "type": "string",
            "enum": ["available", "sold", "pending"]
        },
    }
}

patch_order_response = {
    "type": "object",
    "properties": {
        "message": {
            "type": "string"
        },
        "id": {
            "type": "string", "minimum": 1 #positive ids
        },        
        "pet_id": {
            "type": "integer", "minimum": 1 #positive pet ids
        },   
        "status": {
            "type": "string"
        }
    },
    "required": ["message"],            # Only require what the server actually returns
    "additionalProperties": True        # Set to True since the server might change
}
