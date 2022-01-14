MOCK_OS=fedora-35-x86_64
VERSION=1.0-1.fc35

RESULTS/brother-hl-l8250cdn-${VERSION}.x86_64.rpm : RESULTS/brother-hl-l8250cdn-${VERSION}.src.rpm
	mock -r ${MOCK_OS} --clean --resultdir=RESULTS --rebuild $<

RESULTS/brother-hl-l8250cdn-${VERSION}.src.rpm : brother-hl-l8250cdn.spec
	mock -r ${MOCK_OS} --spec=brother-hl-l8250cdn.spec \
		--sources=./SOURCES --resultdir=RESULTS --buildsrpm
