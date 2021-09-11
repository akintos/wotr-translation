from pf2bp.commontypes import AlignmentShift

from pf2bp import (
    LocalizedString,
    BlueprintRef,
)


class BlueprintBase:
    guid: str
    name: str
    comment: str

    data: object

    def __init__(self, guid, name, data) -> None:
        self.guid = guid
        self.name = name
        self.comment = data["Comment"]

        self.data = data
        self.type: str = data["$type"].split(", ")[0]


class BlueprintAnswer(BlueprintBase):
    text: LocalizedString
    next_cue: list[BlueprintRef]
    alignment_shift: AlignmentShift

    def __init__(self, guid, name, data) -> None:
        super().__init__(guid, name, data)
        self.text = LocalizedString.fromptr(data["Text"])
        self.next_cue = [BlueprintRef(x) for x in data["NextCue"]["Cues"]]
        self.alignment_shift = AlignmentShift(data["AlignmentShift"])


class BlueprintAnswersList(BlueprintBase):
    answers: list[BlueprintRef]

    def __init__(self, guid, name, data) -> None:
        super().__init__(guid, name, data)
        self.answers = [BlueprintRef(x) for x in data["Answers"]]


class BlueprintBookPage(BlueprintBase):
    title: LocalizedString
    cues: list[BlueprintRef]
    answers: list[BlueprintRef]

    def __init__(self, guid, name, data) -> None:
        super().__init__(guid, name, data)
        self.title = LocalizedString.fromptr(data["Title"])
        self.cues = [BlueprintRef(x) for x in data["Cues"]]
        self.answers = [BlueprintRef(x) for x in data["Answers"]]


class BlueprintCue(BlueprintBase):
    text: str
    speaker: BlueprintRef
    answers: list[BlueprintRef]
    continue_cues: list[BlueprintRef]
    alignment_shift: AlignmentShift

    def __init__(self, guid, name, data) -> None:
        super().__init__(guid, name, data)
        self.text = LocalizedString.fromptr(data["Text"])
        self.speaker = BlueprintRef(data["Speaker"]["m_Blueprint"])
        self.answers = [BlueprintRef(x) for x in data["Answers"]]
        self.continue_cues = [BlueprintRef(x) for x in data["Continue"]["Cues"]]
        self.alignment_shift = AlignmentShift(data["AlignmentShift"])


class BlueprintCueSequence(BlueprintBase):
    cues: list[BlueprintRef]
    exit: BlueprintRef
    
    def __init__(self, guid, name, data) -> None:
        super().__init__(guid, name, data)
        self.cues = [BlueprintRef(x) for x in data["Cues"]]
        self.exit = BlueprintRef(data["m_Exit"])


class BlueprintDialog(BlueprintBase):
    first_cue: list[BlueprintRef]

    def __init__(self, guid, name, data) -> None:
        super().__init__(guid, name, data)
        self.first_cue = [BlueprintRef(x) for x in data["FirstCue"]["Cues"]]


class BlueprintCheck(BlueprintBase):
    success: BlueprintRef
    fail: BlueprintRef
    
    checktype: str
    dc: int
    exp: str

    def __init__(self, guid, name, data) -> None:
        super().__init__(guid, name, data)
        self.success = BlueprintRef(data["m_Success"])
        self.fail = BlueprintRef(data["m_Fail"])
        self.checktype = data["Type"]
        self.dc = data.get("DC", 0)
        self.exp = data.get("Experience", "")


class BlueprintSequenceExit(BlueprintBase):
    answers: list[BlueprintRef]
    continue_cues: list[BlueprintRef]

    def __init__(self, guid, name, data) -> None:
        super().__init__(guid, name, data)
        self.answers = [BlueprintRef(x) for x in data["Answers"]]
        self.continue_cues = [BlueprintRef(x) for x in data["Continue"]["Cues"]]

