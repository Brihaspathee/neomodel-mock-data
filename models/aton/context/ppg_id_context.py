from models.aton.nodes.identifier import Identifier


class PPGIDContext(Identifier):

    def __init__(self,  *args, capitated_ppg=None, pcp_required=None, parent_ppg_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        # self.value: str = value
        self.parent_ppg_id: str = parent_ppg_id
        self.capitated_ppg: str = capitated_ppg
        self.pcp_required: str = pcp_required
