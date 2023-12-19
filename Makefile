install:
	pip install pipenv
	pipenv install -r requirements.txt
	pipenv shell
run:
	flask --app app/api run
test:
	pytest tests/	
