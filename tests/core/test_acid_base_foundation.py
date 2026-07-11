from decimal import Decimal
import pytest
from backend.core.chemistry.foundation import AcidSpecies, EquilibriumReaction, EquilibriumType
def test_models() -> None:
    acid=AcidSpecies("A","HA",0,1,Decimal("4"),"A-")
    assert acid.conjugate_species_id=="A-"
    assert EquilibriumReaction(("HA",),("H+","A-"),EquilibriumType.ACID_DISSOCIATION,True).reversible
    with pytest.raises(ValueError): AcidSpecies("A","HA",0,0,Decimal("4"),"A-")
