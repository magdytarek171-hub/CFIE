"""Controlled vocabulary enumerations for immutable formula models."""

from enum import Enum


class ProductType(str, Enum):
    """Approved cosmetic product classifications."""
    CREAM = "Cream"; LOTION = "Lotion"; SERUM = "Serum"; GEL = "Gel"; CLEANSER = "Cleanser"; TONER = "Toner"; SHAMPOO = "Shampoo"; CONDITIONER = "Conditioner"; HAIR_MASK = "Hair Mask"; HAIR_OIL = "Hair Oil"; DEODORANT = "Deodorant"; SUNSCREEN = "Sunscreen"; LIP_PRODUCT = "Lip Product"; MAKEUP = "Makeup"; BODY_WASH = "Body Wash"; BODY_LOTION = "Body Lotion"; OTHER = "Other"


class FormulaStatus(str, Enum):
    """Approved formula lifecycle statuses."""
    DRAFT = "Draft"; IN_REVIEW = "In Review"; APPROVED = "Approved"; ARCHIVED = "Archived"; OBSOLETE = "Obsolete"


class IngredientFunction(str, Enum):
    """Approved functional roles for formula ingredient entries."""
    SOLVENT = "Solvent"; HUMECTANT = "Humectant"; EMOLLIENT = "Emollient"; OCCLUSIVE = "Occlusive"; SURFACTANT = "Surfactant"; EMULSIFIER = "Emulsifier"; CO_EMULSIFIER = "Co-emulsifier"; THICKENER = "Thickener"; RHEOLOGY_MODIFIER = "Rheology Modifier"; PRESERVATIVE = "Preservative"; CHELATING_AGENT = "Chelating Agent"; ANTIOXIDANT = "Antioxidant"; BUFFER = "Buffer"; PH_ADJUSTER = "pH Adjuster"; ACTIVE = "Active"; FRAGRANCE = "Fragrance"; COLORANT = "Colorant"; UV_FILTER = "UV Filter"; SILICONE = "Silicone"; FILM_FORMER = "Film Former"; PEARLIZING_AGENT = "Pearlizing Agent"; OPACIFIER = "Opacifier"; CONDITIONING_AGENT = "Conditioning Agent"; OTHER = "Other"
