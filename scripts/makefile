# Makefile para hacer .so

.SILENT:
all: doSoFile

clone:
	git clone https://github.com/aitorplaza/lib_3d_mec_ginac.git

enter: clone
	mkdir -p lib_3d_mec_ginac/build
	cd lib_3d_mec_ginac && git checkout 75df2fd

doOFile: 
	for f in lib_3d_mec_ginac/lib_3d_mec_ginac/*.cc; do \
		if echo "$$f" | grep -q "Globals_OLD20150830.cc"; then continue; fi; \
		g++ -fPIC -O2 -g -D_FORTIFY_SOURCE=2 -fstack-protector-strong \
			-Ilib_3d_mec_ginac/lib_3d_mec_ginac \
			-I/usr/local/include \
			-c "$$f" \
			-o "lib_3d_mec_ginac/build/$$(basename "$${f%.cc}.o")"; \
	done; \

doSoFile: doOFile
	g++ -shared -Wl,-Bstatic -lginac -lcln -Wl,-Bdynamic -lm -lgcc_s -lc \
		-o lib_3d_mec_ginac/build/lib_3d_mec_ginac.so lib_3d_mec_ginac/build/*o

#Este no parece necesario
#
#stripSo: doSoFile
#	strip --strip-unneeded lib_3d_mec_ginac/build/lib_3d_mec_ginac.so

move: doSoFile
	mv lib_3d_mec_ginac/build/lib_3d_mec_ginac.so pylib3d-mec-ginac/lib/linux/x86_64
	sleep 1

erase:
	rm -rf lib_3d_mec_ginac
