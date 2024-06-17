# A-Complete-LoRaWAN-Image-Transfer
A project that I made on myself for my thesis 1, using library to transfer image from one node to gateway.\
Thanks so much to https://github.com/jeroennijhof/LoRaWAN for providing a free LoRaWAN library for Python.
# What kind of hardwares do you need ?
First of all, 2 Raspberry Pi (any version you like). Any modules which come with the chip SX1276/1277/1278/1279 can be used on this project. Some picture for the hardwares if you're wondering:
![Raspberry Pi 5](https://github.com/buihuy1203/A-Complete-LoRaWAN-Image-Transfer/assets/85066488/b938c7cc-125f-429c-9647-a5ed523dcd9d)
As you can see here this is the Raspberry Pi 5
![Ra-01H](https://github.com/buihuy1203/A-Complete-LoRaWAN-Image-Transfer/assets/85066488/bdb2f7e0-d13d-4171-87ff-061abdea52cd)
This is the module Ra-01H, which supports 868-915MHz. You can find the datasheet here: [Datasheet](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwjcvvm0o-OGAxVHoq8BHZTkCo4QFnoECBMQAQ&url=https%3A%2F%2Fcdn.ozdisan.com%2FETicaret_Dosya%2F632831_134737.pdf&usg=AOvVaw1aTMZMt4EjTAqB1iLpbwlU&opi=89978449)

# How to run
Just simply follow board_config.py in the folder SX1276 to connect the pin to Raspberry Pi.\
After that