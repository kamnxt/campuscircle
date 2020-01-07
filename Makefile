.PHONY: local
local: static/index.html static/style.css elm/src/*.elm pysrc/*.py
	./run_server.sh

static: static/main.js static/index.html static/style.css

python: pysrc/*.py
	mkdir -p python
	cp pysrc/*.py python/

.PHONY: all
all: static python

clean:
	rm -rf static python pysrc/__pycache__ elm/output

.PHONY: upload
upload: all
	rsync -Avz python/*.py mydevil:domains/sophiatime.kamnxt.com/public_python/
	rsync -Avz static/* mydevil:domains/sophiatime.kamnxt.com/public_python/public/

static/main.js: elm/src/*.elm
	mkdir -p static
	cd elm && elm make src/Main.elm --optimize --output=../static/main.js

static/index.html: public/index.html
	mkdir -p static
	cp public/index.html static/index.html

static/style.css: public/style.css
	mkdir -p static
	cp public/style.css static/style.css
