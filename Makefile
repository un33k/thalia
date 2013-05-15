create_env:
	mkdir thalia.env&&cd thalia.env

sync:
	source thalia.env/bin/activate
	pip install -r requirements.txt 

clean:
	find ./ -name '*.pyc' -delete

clean_env:
	rm -rf thalia.env
