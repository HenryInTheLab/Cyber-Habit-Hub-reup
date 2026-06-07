from typing import List

from validate.models import BlacklistedDomains


def blacklist_get(domain: str) -> List[BlacklistedDomains]:
    return list(BlacklistedDomains.objects.filter(domain__iendswith=domain))