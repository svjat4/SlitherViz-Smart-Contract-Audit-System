from schemas.audit import ContractResult, SlitherFinding
from typing import Dict, Any

# Mapping parsial Slither Detector ke SWC ID (Standardisasi Akademik)
SWC_MAPPING = {
    "reentrancy-eth": "SWC-107",
    "reentrancy-no-eth": "SWC-107",
    "uninitialized-state": "SWC-109",
    "tx-origin": "SWC-115",
    "suicidal": "SWC-106",
    "timestamp": "SWC-116",
    "delegatecall-loop": "SWC-112",
}

def calculate_risk_score(counts: dict) -> int:
    """
    Kalkulasi skor berdasarkan bobot ancaman.
    Formula: max(0, 100 - (15*H + 8*M + 3*L + 1*I))
    """
    penalty = (
        15 * counts.get("High", 0) +
        8 * counts.get("Medium", 0) +
        3 * counts.get("Low", 0) +
        1 * counts.get("Informational", 0)
    )
    return max(0, 100 - penalty)

def parse_slither_output(address: str, raw_data: Dict[str, Any]) -> ContractResult:
    result = ContractResult(address=address, status="SUCCESS")
    detectors = raw_data.get("results", {}).get("detectors", [])
    
    for det in detectors:
        impact = det.get("impact", "Informational")
        if impact not in result.severity_counts:
            impact = "Informational" # Fallback
            
        result.severity_counts[impact] += 1
        
        # Ekstrak baris kode yang terdampak
        lines = []
        for elem in det.get("elements", []):
            if "source_mapping" in elem:
                lines.extend(elem["source_mapping"].get("lines", []))
        
        check_name = det.get("check", "unknown")
        
        finding = SlitherFinding(
            name=check_name,
            impact=impact,
            description=det.get("description", ""),
            swc_id=SWC_MAPPING.get(check_name, "N/A"),
            lines=list(set(lines))
        )
        result.findings.append(finding)
        
    result.risk_score = calculate_risk_score(result.severity_counts)
    return result