build:
	docker build -t fitrunner/fitnesse -f Dockerfile .

fitnesse:
	docker run -d fitrunner/fitnesse --mount type=bind,src=/FitNesseRoot,dst=/FitNesseRoot -p 7080:7080
