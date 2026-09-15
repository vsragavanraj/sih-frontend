"""
Legal Metrology Compliance Engine Service

Evaluates product package label fields against the 5 Mandatory Declarations under Legal Metrology Rules:
1. MRP (Maximum Retail Price)
2. Manufacturer Name
3. Net Quantity
4. Manufacturing Date
5. Expiry Date

Compliance Rules:
- If ANY mandatory field is missing: Status = NON_COMPLIANT
- If ALL mandatory fields exist: Status = COMPLIANT

Output JSON Example:
{
  "status": "COMPLIANT",
  "score": 100,
  "missing_fields": []
}
"""

import re
from typing import Dict, Any, List

REQUIRED_FIELDS = [
    "MRP",
    "Manufacturer Name",
    "Net Quantity",
    "Manufacturing Date",
    "Expiry Date"
]

# Field alias lookup for flexible input key matching
FIELD_ALIASES = {
    "MRP": ["mrp", "price", "maximum_retail_price", "retail_price"],
    "Manufacturer Name": ["manufacturer_name", "manufacturer", "mfg_name", "manufacturer_details", "packed_by", "mfg_by"],
    "Net Quantity": ["net_quantity", "net_qty", "quantity", "weight", "net_weight", "volume"],
    "Manufacturing Date": ["manufacturing_date", "mfg_date", "date_of_manufacture", "packing_date", "pkd"],
    "Expiry Date": ["expiry_date", "exp_date", "best_before", "use_by", "shelf_life"]
}

class LegalMetrologyComplianceEngine:
    def validate_fields(self, extracted_fields: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validates extracted package label fields against mandatory Legal Metrology rules.

        Args:
            extracted_fields (Dict[str, Any]): Key-value pair of extracted fields

        Returns:
            Dict containing 'status', 'score', and 'missing_fields':
            {
              "status": "COMPLIANT",
              "score": 100,
              "missing_fields": []
            }
        """
        normalized_input = self._normalize_input_keys(extracted_fields)
        missing_fields: List[str] = []
        present_count = 0
        total_required = len(REQUIRED_FIELDS)

        for required_field in REQUIRED_FIELDS:
            is_present = self._check_field_presence(required_field, normalized_input)
            if is_present:
                present_count += 1
            else:
                missing_fields.append(required_field)

        # Calculate Compliance Score (0 to 100)
        score = int(round((present_count / total_required) * 100))

        # Status Rule: If ANY mandatory field missing -> NON_COMPLIANT; otherwise COMPLIANT
        status_result = "COMPLIANT" if len(missing_fields) == 0 else "NON_COMPLIANT"

        return {
            "status": status_result,
            "score": score,
            "missing_fields": missing_fields
        }

    def _normalize_input_keys(self, input_dict: Dict[str, Any]) -> Dict[str, str]:
        """
        Normalizes input keys to lowercase underscore format for case-insensitive matching.
        """
        normalized = {}
        for k, v in input_dict.items():
            if v is not None:
                str_val = str(v).strip()
                if str_val and str_val.lower() != "n/a" and str_val.lower() != "null":
                    norm_key = k.lower().replace(" ", "_")
                    normalized[norm_key] = str_val
        return normalized

    def _check_field_presence(self, field_name: str, normalized_input: Dict[str, str]) -> bool:
        """
        Checks if a required field or its aliases exist and contain valid non-empty data.
        """
        # Direct check
        direct_key = field_name.lower().replace(" ", "_")
        if direct_key in normalized_input:
            val = normalized_input[direct_key]
            if self._validate_value_format(field_name, val):
                return True

        # Check aliases
        aliases = FIELD_ALIASES.get(field_name, [])
        for alias in aliases:
            if alias in normalized_input:
                val = normalized_input[alias]
                if self._validate_value_format(field_name, val):
                    return True

        return False

    def _validate_value_format(self, field_name: str, value: str) -> bool:
        """
        Validates content quality for each specific required field.
        """
        val_clean = value.strip()
        if not val_clean:
            return False

        if field_name == "MRP":
            # Must contain number or currency symbol
            return bool(re.search(r"(\d|₹|rs)", val_clean, re.IGNORECASE))
        elif field_name in ["Manufacturing Date", "Expiry Date"]:
            # Must contain date pattern or digits/month
            return bool(re.search(r"(\d{2}/\d{2}|\d{2}/\d{4}|\d{4}|\d{2}-\d{2}|\d{2}-\d{4})", val_clean))
        elif field_name == "Net Quantity":
            # Must contain weight/volume digits and units
            return bool(re.search(r"(\d+)", val_clean))
        elif field_name == "Manufacturer Name":
            return len(val_clean) >= 2

        return True

# Global Instance
compliance_engine = LegalMetrologyComplianceEngine()
