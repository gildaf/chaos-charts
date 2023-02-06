# NGC-Monkey
`NGC-Monkey` is a small web app that assists in chaos testing.
It currently supports a small set of commands that allows the test
[probes](https://docs.litmuschaos.io/docs/2.14.0/concepts/probes#comparator) 
to check stateful scenarios.
It uses port 5000 (same as flask tutorial)

## Development
`NGC-Monkey` is a web application written in python based on Flask. 
There is a simple makefile to automate the usual workflow:

* `make build` - build a docker image
* `make run` - run the docker image and expose port 5000
* `make push` - push image to gcr.io/redis-dev-next-gen-cluster
* `make deploy` - deploy the app and a service to k8s (current context and namespace are determined by the local kubectl configuration)
* `make port-for` - start port forwarding for port 5000

For development and local testing you can use `make run` 
or just run the server with your favourite IDE.
Just start a local redis raft and that is it. 
```
export FLOTILLA_DIR="<...>/next-gen/flotilla"
redis-server --loglevel debug --cluster-enabled no --loadmodule "${FLOTILLA_DIR}"/deps/redisraft/redisraft.so --raft.addr 127.0.0.1:6379
redis-cli -c raft.cluster init
```
and the 

### Endpoints
`NGC-Monkey` is web application written in python and use flask.
All connections are synchronous and when there is a need to run a
long task it spawns a thread.


