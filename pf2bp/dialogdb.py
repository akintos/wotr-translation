import json
import os
from pf2bp.commontypes import BlueprintRef

from pf2bp import (
    BlueprintBase,
    BlueprintAnswer,
    BlueprintAnswersList,
    BlueprintBookPage,
    BlueprintCheck,
    BlueprintCue,
    BlueprintCueSequence,
    BlueprintDialog,
    BlueprintSequenceExit,
)

typemapping = {
    "Kingmaker.DialogSystem.Blueprints.BlueprintAnswer": BlueprintAnswer,
    "Kingmaker.DialogSystem.Blueprints.BlueprintAnswersList": BlueprintAnswersList,
    "Kingmaker.DialogSystem.Blueprints.BlueprintBookPage": BlueprintBookPage,
    "Kingmaker.DialogSystem.Blueprints.BlueprintCheck": BlueprintCheck,
    "Kingmaker.DialogSystem.Blueprints.BlueprintCue": BlueprintCue,
    "Kingmaker.DialogSystem.Blueprints.BlueprintCueSequence": BlueprintCueSequence,
    "Kingmaker.DialogSystem.Blueprints.BlueprintDialog": BlueprintDialog,
    "Kingmaker.DialogSystem.Blueprints.BlueprintSequenceExit": BlueprintSequenceExit,
}


class DialogueDatabase:
    bpdict: dict[str, BlueprintBase]
    dialogs: list[BlueprintDialog]

    def __init__(self) -> None:
        self.bpdict = {}
        self.dialogs = []
        pass

    def read_blueprints(self, basedir):
        for dirname in os.listdir(basedir):
            bpcls = typemapping.get(dirname, None)
            if not bpcls: continue
            dirpath = os.path.join(basedir, dirname)
            self._read_bp_directory(dirpath, bpcls)
    
    def _read_bp_directory(self, dirpath, bpcls):
        for filename in os.listdir(dirpath):
            filepath = os.path.join(dirpath, filename)
            name, guid, ext = filename.rsplit(".", 2)
            with open(filepath, "r", encoding="utf-8") as f:
                jsonobj = json.load(f)
            bpobj = bpcls(guid, name, jsonobj)
            self.bpdict[guid] = bpobj
            if bpcls == BlueprintDialog:
                self.dialogs.append(bpobj)

    def getbp(self, ref: BlueprintRef):
        return self.bpdict.get(ref.guid, None)
