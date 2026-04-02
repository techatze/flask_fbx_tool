from job_manager import get_job,update_job
from validator import process_file

def run_job(job_id):
    job = get_job(job_id)

    if not job:
        raise ValueError(f"Job {job_id} not found.")

    update_job(job_id, status="processing")


    try:
        result = process_file(
            job['file'],
            job['process'],
            output_path=job.get('output'),
            axis=job.get('axis')
        )

        update_job(job_id,status='done',result=result)


    except Exception as e:
        update_job(job_id, status='failed', result=str(e))
