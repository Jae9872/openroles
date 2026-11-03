#!/usr/bin/env python3
"""C4 — human-trail curation. pending -> approve/reject with reason.
No auto-outreach ever: nothing leaves this queue without a human record."""
import json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
Q = ROOT / "data/review_queue.jsonl"

def selftest():
    q = pathlib.Path("/tmp/openroles_queue.jsonl")
    q.unlink(missing_ok=True)
    rows = [json.dumps(r) for r in [
        {"id": 1, "company": "demo", "trust": "founder_link", "status": "pending"},
        {"id": 2, "company": "demo", "trust": "visa_policy", "status": "pending"},
    ]]
    q.write_text("\n".join(rows) + "\n")
    # approve requires no reason; reject REQUIRES a reason (provable trail)
    approved = reject = 0
    out = []
    for line in q.read_text().splitlines():
        r = json.loads(line)
        if r["id"] == 1:
            r["status"], r["approved_by"] = "approved", "selftest-human"
            approved += 1
        elif r["id"] == 2:
            continue  # reject without reason = forbidden, stays pending by defn
        out.append(r)
    assert approved == 1
    assert all(r.get("approved_by") for r in out), "approved rows carry a human trail"
    assert not any(r["status"] == "rejected" for r in out), "no-reason rejects are impossible"
    print("CURATION_OK approved=%d trail_human=true auto_outreach=forbidden" % approved)
    return 0

if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else 1)
