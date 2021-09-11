
class LocalizedString:
    key: str
    msg: str

    @classmethod
    def fromptr(cls, ptr: str) -> "LocalizedString":
        _, key, msg = ptr.split(":", 2)
        return cls(key, msg)

    def __init__(self, key: str, msg: str) -> None:
        self.key = key
        self.msg = msg


class BlueprintRef:
    guid: str
    name: str

    def __init__(self, ptr: str) -> None:
        _, self.guid, self.name = ptr.split(":", 2)


class AlignmentShift:
    direction: str
    description: LocalizedString

    def __init__(self, data) -> None:
        self.direction = data["Direction"]
        self.description = LocalizedString.fromptr(data["Description"])
