from flask import Flask,request,jsonify
from job_manager import create_job,get_job,load_jobs
from worker import run_job
import threading

app = Flask(__name__)
load_jobs()

@app.route('/submit',methods=['POST'])
def submit():
    data = request.get_json()

    file_path = data.get("file")
    process = data.get("process")
    output = data.get("output")
    axis = data.get("axis")

    if not file_path or not process:
        return jsonify({"error":"Missing required fields"}),400

    job_id = create_job(
        file_path=file_path,
        process=process,
        output=output,
        axis=axis
    )

    #make job async
    threading.Thread(target = run_job, args = (job_id,)).start()

    return jsonify({
        "job_id":job_id,
        "status":"submitted"
    })


@app.route('/status/<job_id>', methods=['GET'])
def status(job_id):
    job=get_job(job_id)

    if not job:
        return jsonify({"error":"Job not found"}),404

    return jsonify(job)


if __name__ == "__main__":
    app.run(debug=False)