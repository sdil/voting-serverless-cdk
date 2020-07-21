install-python-deps:
	mkdir -p python-deps-layer/python/lib/python3.8/site-packages/
	pip install -r backend/requirements.txt -t python-deps-layer/python/lib/python3.8/site-packages/
