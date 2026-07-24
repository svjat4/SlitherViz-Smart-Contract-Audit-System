from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas.audit import AuditRequest, JobStatusResponse, ContractResult
from services.slither_runner import run_slither_audit
from services.parser import parse_slither_output
import uuid
import asyncio
from typing import Dict

app = FastAPI(title="SlitherViz API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory job store (Untuk produksi: Gunakan Redis + Celery/RQ)
jobs_db: Dict[str, JobStatusResponse] = {}

# PERUBAHAN 1: Tambahkan parameter api_key pada fungsi worker
async def process_audit_batch(job_id: str, addresses: list[str], api_key: str):
    job = jobs_db[job_id]
    total = len(addresses)
    
    for idx, address in enumerate(addresses):
        # PERUBAHAN 2: Teruskan api_key ke Slither
        success, raw_data, err_msg = await run_slither_audit(address, api_key)
        
        if success and raw_data:
            contract_res = parse_slither_output(address, raw_data)
        else:
            contract_res = ContractResult(
                address=address,
                status="FAILED",
                error_message=err_msg
            )
            
        job.results.append(contract_res)
        job.progress = ((idx + 1) / total) * 100
        
    job.status = "COMPLETED"
    jobs_db[job_id] = job

@app.post("/api/audit/batch", response_model=JobStatusResponse)
async def submit_batch_audit(req: AuditRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    jobs_db[job_id] = JobStatusResponse(
        job_id=job_id, status="PROCESSING", progress=0.0, results=[]
    )
    # PERUBAHAN 3: Ambil etherscan_api_key dari request dan kirim ke worker
    background_tasks.add_task(process_audit_batch, job_id, req.addresses, req.etherscan_api_key)
    return jobs_db[job_id]

@app.get("/api/audit/status/{job_id}", response_model=JobStatusResponse)
async def get_job_status(job_id: str):
    if job_id not in jobs_db:
        raise HTTPException(status_code=404, detail="Job not found")
    return jobs_db[job_id]