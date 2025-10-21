from datetime import date
from itertools import groupby

from models.aton.nodes.qualification import Qualification


def _effective_start(q: Qualification) -> date:
    return q.start_date or date.min

def _effective_end(q: Qualification) -> date:
    return q.end_date or date.max

def _is_past(q: Qualification) -> bool:
    return (q.end_date is not None) and (q.end_date < date.today())

def is_active_today(q: Qualification) -> bool:
    return _effective_start(q) <= date.today() <= _effective_end(q)

def _is_future(q: Qualification) -> bool:
    return _effective_start(q) > date.today()

def select_unique_qualifications(qualifications: list[Qualification]) -> list[Qualification]:
    results: list[Qualification] = []
    license_mlc = [q for q in qualifications if q.type == "LICE_MLC"]
    license_mlc.sort(key=lambda q: (q.value, q.state))
    for (value, state), group_iter in groupby(license_mlc, key=lambda q: (q.value, q.state)):
        group = list(group_iter)

        # 1) Discard any of the past records and keep only that are active or in future
        not_past = [q for q in group if not _is_past(q)]
        if not_past:
            continue # all are in the past, so do not keep any licenses

        # 2) Find ones that are active today
        active_today = [q for q in not_past if is_active_today(q)]
        if len(active_today) == 1:
            results.append(active_today[0])
            continue # only one active today so keep only that one
        elif len(active_today) > 1:
            # tie breaker: prefer the one with the latest start date
            # treat NONE (no start date) as date.min so it loses the tie
            chosen = max(active_today, key=lambda q: _effective_start(q))
            results.append(chosen)
            continue
        # 3) no active today — remaining are future/open (because past were removed)
        # The spec: "If none exists then all are future records then set end to
        # greatest and start to earliest"
        # We'll check if all are future; if some are open-ended (start in past
        # but end in future) they'd have been active.
        # So remaining are indeed future (start > today) or open with start > today.
        future_group = [q for q in group if _is_future(q)]
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
            results.append(rep)
            continue
        # Edge case: some remained in not_past but were neither active_today nor future (shouldn't happen
        # given our definitions). As fallback, pick the one with latest effective_end.
        fallback = max(not_past, key=lambda q: _effective_end(q))
        results.append(fallback)
    return results