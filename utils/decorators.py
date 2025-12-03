



from dataclasses import dataclass, field

def opt_field(metadata=None):
    return field(default=None, metadata=metadata or {})


