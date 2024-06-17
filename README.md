# A-Complete-LoRaWAN-Image-Transfer
A project that I made on myself for my thesis 1, using library to transfer image from one node to gateway.\
Thanks so much to [jeroennijhof](https://github.com/jeroennijhof/LoRaWAN) for providing a free LoRaWAN library for Python.
# What is LoRaWAN
Well LoRAWAN is a standard for device using LoRa to communicate, if you want to deep dive, go to Google or Youtube will have a clear explanation about this.#
# What kind of hardwares do you need ?
First of all, 2 Raspberry Pi (any version you like). Any modules which come with the chip SX1276/1277/1278/1279 can be used on this project. Some picture for the hardwares if you're wondering:\
<img src="https://github.com/buihuy1203/A-Complete-LoRaWAN-Image-Transfer/assets/85066488/b938c7cc-125f-429c-9647-a5ed523dcd9d" alt="Raspberry Pi 5" width="250"/>\
As you can see here this is the Raspberry Pi 5.\
![Ra-01H](https://github.com/buihuy1203/A-Complete-LoRaWAN-Image-Transfer/assets/85066488/bdb2f7e0-d13d-4171-87ff-061abdea52cd) \
This is the module Ra-01H, which supports 868-915MHz. You can find the datasheet here: [Datasheet](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwjcvvm0o-OGAxVHoq8BHZTkCo4QFnoECBMQAQ&url=https%3A%2F%2Fcdn.ozdisan.com%2FETicaret_Dosya%2F632831_134737.pdf&usg=AOvVaw1aTMZMt4EjTAqB1iLpbwlU&opi=89978449)\
And also need some antennas so that the LoRa module can communicate with each other. Find them on the market, make sure to find the right frequency.
# How to run
##Step 1:
Install the library cryptodome so that it can encrypt the information.
```bash
pip install pycryptodome
```
##Step 2: 
Just simply follow [board_config.py](LoRaConnection/SX127x/board_config.py) in the folder SX1276 to connect the pin to Raspberry Pi.
```python
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
After that, you are ready to go. Make sure to connect the pins correctly, you can test them through this file [lora_util.py](LoRaConnection/lora_util.py)\
##Step 3: 
You need to check the directories for saving and reading images. This is my directory so remmember to check the directory again\
First in file [LoRaGateWay.py](LoRaReceiver/LoRaGateWay.py) 
```python
if self.receive_frame == 0:
                    print("First Frame")
                    data = json.loads("".join(list(map(chr, lorawan.get_payload()))))
                    with open('/home/huymb/Desktop/receivefile/data.json', 'w') as file:
                        json.dump(data, file, indent=4)
                elif ("".join(list(map(chr, lorawan.get_payload()))))=='End Of Data':
                    print("Save Image")
                    with open('/home/huymb/Desktop/receivefile/result.jpeg', 'wb') as f:
                        f.write(hex_to_image(list_to_hex(self.image_frame)))
                else:
                    self.image_frame.append("".join(list(map(chr, lorawan.get_payload()))))
                    print("Update Frame")
```
And then in file [transferText.py](LoRaConnection/transferText.py)
```python
 data = create_list(hex_to_list(image_to_hex('/home/hieu/Desktop/test.jpeg')))
```
That's all directories you need to fix, we are ready to go
##Step 4:
Simply, running these two files [transferText.py](LoRaConnection/transferText.py) and [LoRaGateWay.py](LoRaReceiver/LoRaGateWay.py), one on a Raspberry Pi, one on other Raspberry Pi and you are good to go.
# Attention
Yes, bugs everywhere, so you should be careful while sending images through LoRa. Sometimes, the data will stop transferring a frame of a picture and the node stops working, so to send it from where it stops, just replace this variable in [transferText.py](LoRaConnection/transferText.py)
```
i = 0 #Replace it with the frame number which was dropped
```
I suggest that if you want to save your time, you should transfer an image which have about 25kB below, so that the connection won't be disconnected and the data won't be corrupted
# That is, you did it
If you send image successfully, congratulations. Although sending image through LoRaWAN is very slow since the payload size of LoRaWAN only about 240 - 245 bytes. But it still transfers successfully, so this is kind like an experiement. And yeah, LoRa can transfer very far long away, so it's still good for transfering short message, don't use this for transferring image if you are doing it commercially.\
Thank you for visiting my project. If any problems happen to the code, just create an issue and I will solve it as soon as possible. And if you like the project, don't forget to add a star. See ya

