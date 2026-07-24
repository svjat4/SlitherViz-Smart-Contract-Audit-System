from pydantic import BaseModel, Field, field_validator
import re
from typing import List, Dict, Optional, Any

class AuditRequest(BaseModel):
    addresses: List[str]
    etherscan_api_key: str # Tambahkan variabel ini

    @field_validator('addresses')
    def validate_addresses(cls, v):
        pattern = re.compile(r'^0x[a-fA-F0-9]{40}$')
        valid_addresses = list(set([addr.lower() for addr in v if pattern.match(addr)]))
        if not valid_addresses:
            raise ValueError("No valid Ethereum addresses provided.")
        return valid_addresses

class SlitherFinding(BaseModel):
    name: str
    impact: str
    description: str
    swc_id: Optional[str] = None
    lines: List[int] = []

class ContractResult(BaseModel):
    address: str
    status: str = Field(pattern="^(SUCCESS|FAILED)$")
    error_message: Optional[str] = None
    risk_score: int = 100
    findings: List[SlitherFinding] = []
    severity_counts: Dict[str, int] = {"High": 0, "Medium": 0, "Low": 0, "Informational": 0, "Optimization": 0}

class JobStatusResponse(BaseModel):
    job_id: str
    status: str = Field(pattern="^(PENDING|PROCESSING|COMPLETED|FAILED)$")
    progress: float
    results: List[ContractResult] = []