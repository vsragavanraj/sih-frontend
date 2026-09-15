"""
Brand Identification & Product Classification Module for LabelGuard AI

Workflow:
OCR Text -> Brand Matching -> Category Detection

Supported Taxonomy:
Food Brands:
- Lays
- Bingo
- Kurkure
- Oreo
- Good Day

Non-Food Brands:
- Lux
- Dove
- Colgate
- Surf Excel
"""

import re
from typing import List, Dict, Any, Optional

BRAND_TAXONOMY = {
    # Food Brands
    "lays": {
        "brand_name": "Lays",
        "product_category": "Food & Beverages",
        "product_type": "Packaged Potato Chips / Snacks",
        "aliases": [r"\blays?\b", r"\blay's\b", r"\bpotato chips\b"]
    },
    "bingo": {
        "brand_name": "Bingo",
        "product_category": "Food & Beverages",
        "product_type": "Packaged Potato Chips & Snacks",
        "aliases": [r"\bbingo\b", r"\bmad angles\b", r"\btedhe medhe\b"]
    },
    "kurkure": {
        "brand_name": "Kurkure",
        "product_category": "Food & Beverages",
        "product_type": "Extruded Corn & Rice Snacks",
        "aliases": [r"\bkurkure\b", r"\bmasala munch\b"]
    },
    "oreo": {
        "brand_name": "Oreo",
        "product_category": "Food & Beverages",
        "product_type": "Cream Biscuit / Confectionery",
        "aliases": [r"\boreo\b", r"\bchocolate cream\b"]
    },
    "good day": {
        "brand_name": "Good Day",
        "product_category": "Food & Beverages",
        "product_type": "Butter / Nut Biscuit",
        "aliases": [r"\bgood\s*day\b", r"\britannia good day\b", r"\bbutter cookies\b"]
    },

    # Non-Food Brands
    "lux": {
        "brand_name": "Lux",
        "product_category": "Personal Care & Cosmetics",
        "product_type": "Beauty Soap / Bathing Bar",
        "aliases": [r"\blux\b", r"\bbeauty soap\b"]
    },
    "dove": {
        "brand_name": "Dove",
        "product_category": "Personal Care & Cosmetics",
        "product_type": "Moisturizing Cream Bar / Shampoo",
        "aliases": [r"\bdove\b", r"\bcream bar\b", r"\bmoisturizing\b"]
    },
    "colgate": {
        "brand_name": "Colgate",
        "product_category": "Personal Care & Cosmetics",
        "product_type": "Oral Hygiene / Toothpaste",
        "aliases": [r"\bcolgate\b", r"\bstrong teeth\b", r"\bmax fresh\b", r"\btoothpaste\b"]
    },
    "surf excel": {
        "brand_name": "Surf Excel",
        "product_category": "Home Care & Cleaning",
        "product_type": "Detergent Powder / Liquid",
        "aliases": [r"\bsurf\s*excel\b", r"\bsurf\b", r"\beasy wash\b", r"\bdetergent\b"]
    }
}

class BrandIdentifier:
    def __init__(self):
        self.taxonomy = BRAND_TAXONOMY

    def identify_brand(self, text_input: Any) -> Dict[str, Any]:
        """
        Executes Brand Identification Workflow:
        OCR Text -> Brand Matching -> Category Detection

        Args:
            text_input: Can be full text string, list of text blocks, or filename string.

        Returns:
            Dict containing brand_name, product_category, product_type, and confidence.
        """
        if isinstance(text_input, list):
            search_str = " ".join(text_input).lower()
        else:
            search_str = str(text_input).lower()

        # Iterate through brand taxonomy regex aliases
        for key, info in self.taxonomy.items():
            for alias_pattern in info["aliases"]:
                if re.search(alias_pattern, search_str, re.IGNORECASE):
                    return {
                        "brand_name": info["brand_name"],
                        "product_category": info["product_category"],
                        "product_type": info["product_type"],
                        "confidence": 0.96,
                        "matched_keyword": key
                    }

        # Fallback for unlisted / generic organic products
        return {
            "brand_name": "Generic Packaged Goods",
            "product_category": "Food & Commodities",
            "product_type": "Pre-Packaged Retail Commodity",
            "confidence": 0.80,
            "matched_keyword": "generic"
        }

# Global Service Instance
brand_identifier = BrandIdentifier()
