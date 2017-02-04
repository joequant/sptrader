MAJOR_VERSION=8
MINOR_VERSION=742
ZIP_FILE=SPAPIDLL_R${MAJOR_VERSION}.${MINOR_VERSION}_LINUX.zip

../dll/linux-shim.so: linux-shim.cpp ../dll/libapiwrapper.so
	g++ --std=c++14 -g -shared -o ../dll/linux-shim.so -fPIC linux-shim.cpp

../dll/libapiwrapper.so: ${ZIP_FILE}
	rm -rf lib include
	unzip ${ZIP_FILE}
	mv lib/libapiwrapper.so ../dll
	touch ../dll/libapiwrapper.so
	rm -rf lib include

${ZIP_FILE}:
	wget http://spsystem.info/download/API/R${MAJOR_VERSION}${MINOR_VERSION}/${ZIP_FILE}

clean:
	rm -rf ${ZIP_FILE} ../dll/libapiwrapper.so ../dll/linux-shim.so

.DUUMY: clean
