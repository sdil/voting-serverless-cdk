include frontend/.env
export

install-python-deps:
	mkdir -p python-deps-layer/python/lib/python3.8/site-packages/
	pip install -r backend/requirements.txt -t python-deps-layer/python/lib/python3.8/site-packages/

deploy-frontend:
	cd frontend && npm run build && nuxt export
	cdk diff voting-frontend-cdk
	cdk deploy voting-frontend-cdk

dev-frontend:
	cd frontend && npm run dev

build-frontend:
	cd frontend && npm run build && nuxt export && nuxt serve
