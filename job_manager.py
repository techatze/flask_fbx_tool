import uuid
import json

jobs = {}

def create_job(file_path, process, output=None, axis=None):
    job_id = str(uuid.uuid4())
    print(job_id)

    jobs[job_id]={
        "id":job_id,
        "file":file_path,
        "process":process,
        "status":"queued",
        "result":None
    }
    save_jobs()
    return job_id


def get_job(job_id):
    return jobs.get(job_id)


def update_job(job_id, **kwargs):
    if job_id in jobs:
        jobs[job_id].update(kwargs)
        save_jobs()


def save_jobs():
    with open("jobs.json", "w") as f:
        json.dump({"jobs": list(jobs.values())}, f, indent=4)


def load_jobs():
    global jobs

    try:
        with open("jobs.json","r") as f:
            data = json.load(f)

            jobs = {job["id"]: job for job in data["jobs"]}

    except FileNotFoundError:
        jobs={}