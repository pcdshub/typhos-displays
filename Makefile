adcore_clone:
	@if [[ ! -d adcore ]]; then \
		git clone https://github.com/areaDetector/adcore && \
		echo "ADCore cloned."; \
	fi
	@echo "ADCore available."

adcore_convert:
	convert_path=$${PWD}/conversion; \
	pushd adcore; \
		for release in $$(git tag |grep -v -e beta); do \
			echo "\n**** $${release} ****"; \
			git reset --hard $${release}; \
			rm -f $${convert_path}/*.ui; \
			adl2pydm -d $${convert_path} $$(find . -name "*.adl"); \
			pushd $${convert_path} && \
				python rename_converted_adcore.py $${release}; \
			popd; \
		done; \
	popd
