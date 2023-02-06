PORT=5000
SERVER_APP=ngc-monkey-server

build:
	docker build -f Dockerfile.server -t $(SERVER_APP) .

run: build
	docker run -p $(PORT):$(PORT) -it $(SERVER_APP)

push: build
	docker tag $(SERVER_APP) gcr.io/redis-dev-next-gen-cluster/$(SERVER_APP)
	docker push gcr.io/redis-dev-next-gen-cluster/$(SERVER_APP)

deploy:
	kubectl apply -f k8s/deployment.yaml

undeploy:
	kubectl delete -f k8s/deployment.yaml

port-for:
	kubectl port-forward service/ngc-monkey $(PORT):$(PORT)