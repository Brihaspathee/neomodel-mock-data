class OrganizationContext:

    def __init__(self):
        self.pending_is_bh = False
        self.pending_is_pcp = False
        self.pending_is_specialist = False

    def __repr__(self):
        return f"<OrganizationContext:(" \
               f"is_bh={self.pending_is_bh}, " \
               f"is_pcp={self.pending_is_pcp}, " \
               f"is_specialist={self.pending_is_specialist})>"