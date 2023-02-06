import typing

import flask
from flask import Flask, request

from .raft_client import RaftClient
from .traffic_generator import TrafficGenerator

app = Flask(__name__)
_threads = {}


@app.route('/run', methods=['POST'])
def run():
    """
    Start a task (spawn a thread) that pushes keys
    to redis and remember each key that was successfully set.
    :param: db_name (String) the host name of the Redis Database
    :return: 202 on success
             500 on failure
             409 if there is already a running task for the given db_name
    """
    db_name = request.json.get("db_name")
    tg: typing.Optional[TrafficGenerator] = _threads.get(db_name)
    if tg and tg.is_alive():
        flask.abort(409, f"Traffic generation is already in progress for db {db_name}")
    tg = TrafficGenerator(host=db_name)
    try:
        tg.redis_con.assert_raft_is_up()
    except Exception as e:
        flask.abort(500, f"Failed to connect to redis {db_name}. {str(e)}")

    tg.start()
    _threads[db_name] = tg
    return flask.jsonify(201)


@app.route('/check', methods=['POST'])
def check():
    """
    Stop the thread connected to db_name and wait until it exits.
    Then go over all keys that were sent, and assert that the DB has the correct value for them.
    :param: db_name (String) the host name of the Redis Database
    :return: 200 if the db_name has a running thread and result of the form `{ "result": "success" or "failure" }`
             404 if the db_name does is not known
    """
    db_name = request.json.get("db_name")
    traffic_gen: TrafficGenerator = _threads.get(db_name)
    if traffic_gen is None:
        flask.abort(404, description=f"DB {db_name} not found")
    traffic_gen.stop_traffic()
    traffic_gen.join(5.0)
    result = traffic_gen.check()
    status_code = 200 if result.is_success() else 500
    return flask.jsonify({"result": f"{result}"}), status_code


@app.route('/raft_info', methods=['POST'])
def raft_info():
    db_name = request.json.get("db_name")
    redis_con = RaftClient(host=db_name, decode_responses=True)
    return flask.jsonify(redis_con.raft_info(target_nodes=RaftClient.PRIMARIES))


@app.route("/hello", methods=['POST', 'GET'])
def hello():
    return "Hello, World!"
