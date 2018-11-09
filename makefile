SHELL := /bin/bash
build:
	docker build -t fitrunner/fitnesse -f Dockerfile .

fitnesse:
	docker rm -f fitrunner-fitnesse | true
	docker run -d --name fitrunner-fitnesse --mount type=bind,src=$$(pwd)/FitNesseRoot,dst=/FitNesseRoot -p 7080:7080 fitrunner/fitnesse
