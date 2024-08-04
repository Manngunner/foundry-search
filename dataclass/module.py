from dataclasses import dataclass

@dataclass
class Module:
    """Class for Foundry VTT modules."""
    module_id: int
    name: str
    title: str
    description: str
    url: str
    is_exclusive: bool # Exclusive to FoundryVTT
    is_protected: bool # Hidden manifest?? Paid-for mods
    author_username: str
    tags: list[list[str]]
    systems: list[str]
    compatible_generation: int
    minimum: str
    verified: str
    maximum: str
    requires: list[str]

    version: dict[int, str]