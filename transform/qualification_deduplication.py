from datetime import date
from itertools import groupby
from operator import attrgetter
from typing import Optional

from models.aton.nodes.qualification import Qualification
from config.qualification_rules_settings import QUALIFICATION_RULES
import logging

log = logging.getLogger(__name__)


def _effective_start(q: Qualification) -> date:
    return q.start_date or date.min

def _effective_end(q: Qualification) -> date:
    return q.end_date or date.max

def _is_past(q: Qualification) -> bool:
    today: date = date.today()
    return (q.end_date is not None) and (q.end_date < today)

def is_active_today(q: Qualification) -> bool:
    return _effective_start(q) <= date.today() <= _effective_end(q)

def _is_future(q: Qualification) -> bool:
    return _effective_start(q) > date.today()

def select_unique_qualifications(qualifications: list[Qualification]) -> list[Qualification]:
    log.info(f"Qualification rules:{QUALIFICATION_RULES}")
    results: list[Qualification] = []
    # Group qualifications by type
    qualifications.sort(key=attrgetter('type'))
    for qual_type, group_iter in groupby(qualifications, key=attrgetter('type')):
        group = list(group_iter)
        if qual_type not in QUALIFICATION_RULES:
            log.info(f"Qualification type {qual_type} not in rules, keeping all")
            continue
        type_rule = QUALIFICATION_RULES[qual_type]
        unique_keys = type_rule.get("unique_keys", [])
        selection_rule = type_rule.get("selection_rule", "temporal")

        # Sort + group by unique key values
        group.sort(key=lambda q: tuple(getattr(q, key) for key in unique_keys))
        for key_values, sub_iter in groupby(group, key=lambda q: tuple(getattr(q, key) for key in unique_keys)):
            sub_group = list(sub_iter)
            if selection_rule == "temporal":
                chosen: Qualification = _apply_temporal_selection_rule(sub_group)
                if chosen:
                    results.append(chosen)
    return update_qualification_list(qualifications, results)

def _apply_temporal_selection_rule(group: list[Qualification]) -> Optional[Qualification]:

    # 1) Discard any of the past records and keep only that are active now or in future
    not_past = [q for q in group if not _is_past(q)]
    if not not_past:
        return None # all are in the past, so do not keep any qualifications of this type

    # 2) Find ones that are active today
    active_today = [q for q in not_past if is_active_today(q)]
    if len(active_today) == 1:
        return active_today[0] # only one active today so keep only that one
    elif len(active_today) > 1:
        # tie breaker: prefer the one with the latest start date
        # treat NONE (no start date) as date.min so it loses the tie
        chosen = max(active_today, key=lambda q: _effective_start(q))
        return chosen
    # 3) no active today — remaining are future/open (because past were removed)
    # The spec: "If none exists then all are future records then set end to
    # greatest and start to earliest"
    # We'll check if all are future; if some are open-ended (start in past
    # but end in future) they'd have been active.
    # So remaining are indeed future (start > today) or open with start > today.
    future_group = [q for q in not_past if _is_future(q)]
    if future_group:
        # compute earliest start and latest end among future_group
        # For earliest start: choose the minimum of non-None starts; if any start is None,
        # treat as date.min (but that wouldn't be future)

        min_start = min((q.start_date for q in future_group if q.start_date is not None), default=None)
        max_end = max((q.end_date for q in future_group if q.end_date is not None), default=None)
        # take a representative (shallow copy) and set merged dates
        rep = future_group[0]

        rep.start_date = min_start
        rep.end_date = max_end
        return rep
    # Edge case: some remained in not_past but were neither active_today nor future (shouldn't happen
    # given our definitions). As fallback, pick the one with latest effective_end.
    return max(not_past, key=_effective_end)

def update_qualification_list(original_list: list[Qualification], de_duped_quals: list[Qualification]):
    if de_duped_quals:
       updated_quals = []
       for qual in original_list:
           # If this qualification type is not present in the qualification results, add it
           if not any(q.type == qual.type for q in de_duped_quals):
               updated_quals.append(qual)
       updated_quals.extend(de_duped_quals)
       return updated_quals
    else:
        return original_list