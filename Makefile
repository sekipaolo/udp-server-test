IMAGE=upd-server-test
PORT=1234
.PHONY: build test

build:
	docker build -t ${IMAGE} .

run: build
	docker run -e LISTEN_PORT=$PORT -p $PORT:$PORT/udp -i ${IMAGE} python ./server.py
