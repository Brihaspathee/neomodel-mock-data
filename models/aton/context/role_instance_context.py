import weakref

from models.aton.nodes.disorder import Disorder
from models.aton.nodes.healthcare_service import HealthcareService
from models.aton.nodes.role_instance import RoleInstance
from models.aton.nodes.role_location import RoleLocation
from models.aton.nodes.role_network import RoleNetwork
from models.aton.nodes.role_specialty import RoleSpecialty


class RoleInstanceContext:

    def __init__(self, role_instance:RoleInstance):
        self.role_instance = weakref.proxy(role_instance)
        self._role_type: str | None = None
        self._rls: list[RoleLocation] = []
        self._rns: list[RoleNetwork] = []
        self._prac_rs: list[RoleSpecialty] = []
        self._prac_disorders: list[Disorder] = []
        self._prac_hs: list[HealthcareService] = []

    def set_role_type(self, role_type: str):
        self._role_type = role_type

    def get_role_type(self):
        return self._role_type

    def add_rl(self, rl: RoleLocation):
        self._rls.append(rl)

    def get_rls(self) -> list[RoleLocation]:
        return self._rls

    def add_rn(self, rn: RoleNetwork):
        self._rns.append(rn)

    def get_rns(self) -> list[RoleNetwork]:
        return self._rns

    def add_prac_rs(self, prac_rs: RoleSpecialty):
        self._prac_rs.append(prac_rs)

    def get_prac_rs(self) -> list[RoleSpecialty]:
        return self._prac_rs

    def add_prac_disorders(self, prac_disorders: Disorder):
        self._prac_disorders.append(prac_disorders)

    def get_prac_disorders(self) -> list[Disorder]:
        return self._prac_disorders

    def add_prac_hs(self, prac_hs: HealthcareService):
        self._prac_hs.append(prac_hs)

    def get_prac_hs(self) -> list[HealthcareService]:
        return self._prac_hs