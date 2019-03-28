all: build

build: build/kiosk

build/kiosk: src/content/resource.py src/kiosk.py src/*.py Makefile
	mkdir -p build
	python -m zipapp src -m "kiosk:main" -o build/kiosk -c -p "/usr/bin/env python3"


src/content/resource.py: qml/kiosk.qrc qml/Kiosk.qml Makefile qml/qtquickcontrols2.conf qml/img/* qml/pages/*.qml
	~/.local/bin/pyside2-rcc -o src/content/resource.py  -compress 9 -threshold 1 qml/kiosk.qrc



upload: build/kiosk forms/* 
	scp build/kiosk root@kiosk.multidat.ru:/opt/kiosk/build/
	scp forms/* root@kiosk.multidat.ru:/opt/kiosk/forms/
	touch upload
