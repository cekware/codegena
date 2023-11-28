

from dataclasses import dataclass

@dataclass(unsafe_hash=True)
class SwiftModuleImport:
    name: str
    function_name: str
    extra_info: dict






