# A-Complete-LoRaWAN-Image-Transfer
A project that I made on myself for my thesis 1, using library to transfer image from one node to gateway.\
Thanks so much to https://github.com/jeroennijhof/LoRaWAN for providing a free LoRaWAN library for Python.
# What kind of hardwares do you need ?
First of all, 2 Raspberry Pi (any version you like). Any modules which come with the chip SX1276/1277/1278/1279 can be used on this project. Some picture for the hardwares if you're wondering:
![Raspberry Pi 5](https://github.com/buihuy1203/A-Complete-LoRaWAN-Image-Transfer/assets/85066488/b938c7cc-125f-429c-9647-a5ed523dcd9d)
As you can see here this is the Raspberry Pi 5.\
![Ra-01H](https://github.com/buihuy1203/A-Complete-LoRaWAN-Image-Transfer/assets/85066488/bdb2f7e0-d13d-4171-87ff-061abdea52cd) \
This is the module Ra-01H, which supports 868-915MHz. You can find the datasheet here: [Datasheet](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwjcvvm0o-OGAxVHoq8BHZTkCo4QFnoECBMQAQ&url=https%3A%2F%2Fcdn.ozdisan.com%2FETicaret_Dosya%2F632831_134737.pdf&usg=AOvVaw1aTMZMt4EjTAqB1iLpbwlU&opi=89978449)\
And also need some antennas so that the LoRa module can communicate with each other. Find them on the market, make sure to find the right frequency.
# How to run
Just simply follow [board_config.py](board_config.py) in the folder SX1276 to connect the pin to Raspberry Pi.\
```
 # Note that the BCOM numbering for the GPIOs is used.
    DIO0 = 22   # RaspPi GPIO 22
    DIO1 = 23   # RaspPi GPIO 23
    DIO2 = 24   # RaspPi GPIO 24
    DIO3 = 25   # RaspPi GPIO 25
    LED  = 18   # RaspPi GPIO 18 connects to the LED on the proto shield
    SWITCH = 4  # RaspPi GPIO 4 connects to a switch

    # The spi object is kept here
    spi = None
    
    # tell pySX127x here whether the attached RF module uses low-band (RF*_LF pins) or high-band (RF*_HF pins).
    # low band (called band 1&2) are 137-175 and 410-525
    # high band (called band 3) is 862-1020
    low_band = False
```
After that, you are ready to go
