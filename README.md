# Internet Connected Humidor

## System Configuration

#### Prerequisites
```bash
curl -sLS https://apt.adafruit.com/add | sudo bash
sudo apt-get update
sudo apt-get install node npm build-essential python-dev git scons swig
npm install aws-iot-device-sdk
```

#### https://github.com/adafruit/Adafruit_Python_SSD1306
```bash
git pull https://github.com/adafruit/Adafruit_Python_SSD1306.git
cd Adafruit_Python_SSD1306 && sudo python setup.py install && sudo python3 setup.py install
```

#### Python WS281x/Neopixel Driver
```bash
cd ~
git clone https://github.com/jgarff/rpi_ws281x.git
cd rpi_ws281x
scons
cd python
sudo python setup.py install && sudo python3 setup.py install
```

## Hardware Setup

### Raspberry Pi Zero-w Pin Setup

|	Pin		|	RPi Function / Name		|	Connected To				|
|-----------|---------------------------|-------------------------------|
| Pin 01	|	3.3v 					|	3.3v BUS					|
| Pin 02	|	5v						|	NC							|
| Pin 03	|	BCM-02	(i2c SDA)		|	i2c SDA BUS (to TCA9548A)	|
| Pin 04	|	5v						|	NC							|
| Pin 05	|	BCM-03	(i2c SCL)		|	i2c SCL BUS (to TCA9548A)	|
| Pin 06	|	Ground					|	Ground BUS					|
| Pin 07	|	BCM-04	(GPCLK0)		|	NC							|
| Pin 08	|	BCM-14	(TxD)			|	NC							|
| Pin 09	|	Ground					|	Ground BUS					|
| Pin 10	|	BCM-15	(RxD)			|	NC							|
| Pin 11	|	BCM-17	(SPI-1 CE1)		|	NC							|
| Pin 12	|	BCM-18	(SPI-1 CE0)		|	NC							|
| Pin 13	|	BCM-27					|	NC							|
| Pin 14	|	Ground					|	Ground BUS					|
| Pin 15	|	BCM-22					|	NC							|
| Pin 16	|	BCM-23					|	SSD1306 Display DC			|
| Pin 17	|	3.3v					|	3.3v BUS					|
| Pin 18	|	BCM-24					|	SSD1306 Reset pin			|
| Pin 19	|	BCM-10	(SPI-0 MOSI)	|	SSD1306 MOSI/SDI (D1)		|
| Pin 20	|	Ground					|	Ground BUS					|
| Pin 21	|	BCM-09	(SPI-0 MISO)	|	NC							|
| Pin 22	|	BCM-25					|	NC							|
| Pin 23	|	BCM-11	(SPI-0 SCLK)	|	SSD1306 SCK (D0)			|
| Pin 24	|	BCM-08	(SPI-0 CE0)		|	SSD1306 CS					|
| Pin 25	|	Ground					|	Ground BUS					|
| Pin 26	|	BCM-07	(SPI-0 CE1)		|	NC							|
| Pin 27	|	BCM-00	(ID_SD)			|	NC							|
| Pin 28	|	BCM-01	(ID_SC)			|	NC							|
| Pin 29	|	BCM-05					|	Door open Sensor			|
| Pin 30	|	Ground					|	Ground BUS					|
| Pin 31	|	BCM-06					|	PIR Sensor Output			|
| Pin 32	|	BCM-12	(PWM-0)			|	NeoPixel					|
| Pin 33	|	BCM-13	(PWM-1)			|	NC							|
| Pin 34	|	Ground					|	Ground BUS					|
| Pin 35	|	BCM-19	(SPI-1 MISO)	|	NC							|
| Pin 36	|	BCM-16	(SPI-1 CE2)		|	NC							|
| Pin 37	|	BCM-26					|	NC							|
| Pin 38	|	BCM-20	(SPI-1 MOSI)	|	NC							|
| Pin 39	|	Ground					|	Ground BUS					|
| Pin 40	|	BCM-21	(SPI-1 SLCK)	|	NC							|


### SSD1306
[Sparkfun Micro OLED Breakout](https://www.sparkfun.com/products/13003)

|	Pin		|	Conneted To	|
|-----------|---------------|
| Pin GND	|	Ground BUS	|
| Pin 3v3	|	3.3v BUS	|
| Pin D1	|	RPI Pin 19	|
| Pin D0	|	RPI Pin 23	|
| Pin D2	|	NC			|
| Pin D/C	|	RPI Pin 16	|
| Pin RST	|	RPI Pin 18	|
| Pin CS	|	RPI Pin 24	|

TCA9548A
[Adafruit TCA9548A breakout](https://www.adafruit.com/product/2717)

|	PIN		|	Connected To			|
|-----------|---------------------------|
| Pin VIN	|	3.3v BUS				|
| Pin GND	|	Ground BUS				|
| Pin SDA	|	i2c SDA BUS				|
| Pin SCL	|	i2c SCL BUS				|
| Pin RST	|	NC						|
| Pin A0	|	4.7K Resistor to GROUND	|
| Pin A1	|	4.7K Resistor to GROUND	|
| Pin A2	|	4.7K Resistor to GROUND	|
| PIN SD0	|	SI7021 Sensor SDA		|
| PIN SC0	|	SI7021 Sensor SCL		|
| PIN SD1	|	SI7021 Sensor SDA		|
| PIN SC1	|	SI7021 Sensor SCL		|
| PIN SD2	|	SI7021 Sensor SDA		|
| PIN SC2	|	SI7021 Sensor SCL		|
| PIN SD3	|	NC						|
| PIN SC3	|	NC						|
| PIN SD4	|	NC						|
| PIN SC4	|	NC						|
| PIN SD5	|	NC						|
| PIN SC5	|	NC						|
| PIN SD6	|	NC						|
| PIN SC6	|	NC						|
| PIN SD7	|	NC						|
| PIN SC7	|	NC						|





