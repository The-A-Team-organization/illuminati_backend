from enum import Enum
from enums.roles import Role, VoteEnum


class VoteRules:

    rules = {
        'Mason' : "PROMOTE_TO_SILVER",
        'SilverMason' : "PROMOTE_TO_GOLDEN",
        'GoldMason' : "PROMOTE_TO_ARCHITECT"
    }

class PromoteRules:

    rules = {
        "PROMOTE_TO_SILVER" : Role.SILVER_MASON,
        "PROMOTE_TO_GOLDEN" : Role.GOLD_MASON,
        "PROMOTE_TO_ARCHITECT" : Role.ARCHITECT
    }