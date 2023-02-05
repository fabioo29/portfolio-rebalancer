build-local:
	docker build . -t portfolio-rebalancer:latest

push-image:
	docker save portfolio-rebalancer:latest | gzip > portfolio-rebalancer.tar.gz
	scp portfolio-rebalancer.tar.gz ${host}:
	rm -f portfolio-rebalancer.tar.gz
	ssh ${host} "zcat portfolio-rebalancer.tar.gz | sudo docker load"
	ssh ${host} "sudo docker system prune -f"
	ssh ${host} "rm -f portfolio-rebalancer.tar.gz"

deploy-host:
	ssh ${host} "sudo docker rm portfolio-rebalancer -f || true"
	ssh ${host} "sudo docker run -d --restart=always --name portfolio-rebalancer portfolio-rebalancer:latest"

run-pipeline:
	make build-local
	make push-image
	make deploy-host