install:
	wget abyz.co.uk/rpi/pigpio/pigpio.zip
	unzip pigpio.zip && rm pigpio.zip
	mv PIGPIO/* src && rmdir PIGPIO
	git clone https://github.com/roberttidey/LightwaveRF.git
	cp LightwaveRF/Raspberry/c-custom/* src
	cd src && make && sudo make install && cd ..

.PHONY: install
