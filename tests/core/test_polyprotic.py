"""Tests for ES-007 structural polyprotic models."""
from decimal import Decimal
import pytest
from backend.core.chemistry.polyprotic import DissociationStep, PolyproticAcid, SpeciesRecord, SpeciesSequence

def _model() -> PolyproticAcid:
    species=SpeciesSequence((SpeciesRecord("a","A",0,0),SpeciesRecord("b","B",-1,1)))
    step=DissociationStep(1,Decimal("4"),"a","b")
    return PolyproticAcid("Test","A",Decimal("100"),0,1,(Decimal("4"),),("b",),species,(step,))

def test_valid_chain() -> None:
    assert _model().conjugate_species_ids == ("b",)

def test_rejects_charge_progression() -> None:
    species=SpeciesSequence((SpeciesRecord("a","A",0,0),SpeciesRecord("b","B",0,1)))
    with pytest.raises(ValueError, match="decrease"):
        PolyproticAcid("Test","A",Decimal("100"),0,1,(Decimal("4"),),("b",),species,(DissociationStep(1,Decimal("4"),"a","b"),))
