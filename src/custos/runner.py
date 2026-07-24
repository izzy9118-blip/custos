from __future__ import annotations
from pathlib import Path
from typing import Any
from datetime import datetime, timezone
import json, shlex, subprocess
from .config import load_config, load_yaml
from .validation import validate_repository

def git_head(root: Path) -> str:
    try:
        result=subprocess.run(["git","-C",str(root),"rev-parse","HEAD"],check=True,capture_output=True,text=True,timeout=10)
        return result.stdout.strip()
    except Exception:
        return "UNAVAILABLE"

def build_request(root: Path) -> dict[str, Any]:
    validation=validate_repository(root)
    config=load_config(root)
    inquiry_dir=root/config["active_inquiry"]
    protocol=load_yaml(root/config["reading_protocol"])
    taxonomy=load_yaml(root/config["literary_techniques"])
    evidence=load_yaml(inquiry_dir/"evidence.yaml")
    status=load_yaml(inquiry_dir/"status.yaml")
    excerpts=[]
    for item in evidence["evidence"]:
        excerpts.append({**item,"text":(root/item["path"]).read_text(encoding="utf-8")})
    return {
      "contract":"custos.analysis-request.v1",
      "repository_commit":git_head(root),
      "instructions_path":config["instructions"],
      "protocol":protocol,
      "literary_techniques":taxonomy,
      "inquiry":{"path":config["active_inquiry"],"status":status,"text":(inquiry_dir/"inquiry.md").read_text(encoding="utf-8")},
      "evidence":excerpts,
      "validation":validation,
      "required_response":{"summary":"string","documented_findings":"array","supported_inference":"string or null","strongest_alternative":"string or null","technique_evaluations":"array","uncertainties":"array","next_textual_act":"string"}
    }

def analyze(root: Path, output: Path, reasoner_command: str | None=None) -> Path:
    request=build_request(root)
    output.mkdir(parents=True,exist_ok=False)
    (output/"analysis-request.json").write_text(json.dumps(request,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    result={"status":"READY_FOR_REASONER","repository_commit":request["repository_commit"]}
    if reasoner_command:
        proc=subprocess.run(shlex.split(reasoner_command),input=json.dumps(request),capture_output=True,text=True,timeout=300)
        if proc.returncode != 0:
            raise RuntimeError(f"Reasoner failed ({proc.returncode}): {proc.stderr.strip()}")
        response=json.loads(proc.stdout)
        if not isinstance(response,dict) or not isinstance(response.get("summary"),str):
            raise ValueError("Reasoner response must be an object with a string summary")
        (output/"analysis-response.json").write_text(json.dumps(response,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        result["status"]="COMPLETED"
    result["created_at"]=datetime.now(timezone.utc).isoformat()
    (output/"run.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    return output

def sanctum_report(root: Path, envelope_path: Path, output: Path) -> Path:
    request=build_request(root)
    envelope=json.loads(envelope_path.read_text(encoding="utf-8"))
    if not isinstance(envelope,dict) or not envelope.get("question") or envelope.get("inquiry_id") != request["inquiry"]["status"]["inquiry_id"]:
        raise ValueError("Envelope must name the active inquiry_id and a nonempty question")
    status=request["inquiry"]["status"]
    report={"contract":"custos.sanctum-report.v1","inquiry_id":envelope["inquiry_id"],"question":envelope["question"],"repository_commit":request["repository_commit"],"governing_instruction":"CUSTOS.md","reading_protocol":"protocol/reading.yaml","evidence":[{"id":i["id"],"path":i["path"],"sha256":i["sha256"],"limitations":i["limitations"]} for i in request["evidence"]],"current_state":status,"report_status":"CANDIDATE_NOT_CERTIFIED","limitations":["This report does not certify an interpretation.","Custos retains its corpus and internal inquiry record."]}
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return output
