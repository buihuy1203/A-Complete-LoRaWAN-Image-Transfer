import sys
from time import sleep
from SX127x.LoRa import *
import LoRaWAN
from LoRaWAN.MHDR import MHDR
from SX127x.board_config import BOARD
from SX127x.constants import *
from CollectData import *

BOARD.setup()

class LoRaSend(LoRa):
    tx_counter = 0
    def __init__(self, devaddr = [], nwkey = [], appkey = [], verbose=True):
        super(LoRaSend, self).__init__(verbose)
        self.devaddr=devaddr
        self.nwkey=nwkey
        self.appkey=appkey
        self.rx_packet =[]
    def on_tx_done(self):
        print("TxDone")
        self.clear_irq_flags(TxDone=1)
        self.set_mode(MODE.STDBY)
        self.set_dio_mapping([0,0,0,0,0,0])
        self.reset_ptr_rx()
        BOARD.led_off()
        self.clear_irq_flags(RxDone=1)
        self.set_mode(MODE.RXCONT)
    def on_rx_done(self):
        self.reset_ptr_rx()
        BOARD.led_on()
        print("RxDone")
        self.rx_packet = self.read_payload(nocheck=True)
        self.set_mode(MODE.STDBY)
        self.clear_irq_flags(RxDone=1)
    def start(self):
        lorawan = LoRaWAN.new(nwskey, appskey)
        while True:
            data = create_list(hex_to_list(image_to_hex('/home/hieu/Desktop/test.jpeg')))
            i = 0
            while i < len(data):
                self.tx_counter=0
                lorawan.create(MHDR.UNCONF_DATA_UP, {'devaddr': devaddr, 'fcnt': i, 'data': list(map(ord,data[i]))})
                sys.stdout.write("\rStart data " + data[i] +" and frame number "+str(i)+"\n")
                BOARD.led_on()
                self.rx_packet=[]
                self.set_dio_mapping([1,0,0,0,0,0])
                self.set_mode(MODE.STDBY)
                self.clear_irq_flags(TxDone=1)
                sleep(.5)
                self.write_payload(lorawan.to_raw())
                self.set_mode(MODE.TX)
                sleep(5)
                while (self.tx_counter <= 3):
                    if self.rx_packet!=[]:
                        print(self.rx_packet)
                        lorawan.read(self.rx_packet)
                        print("".join(list(map(chr,lorawan.get_payload()))))
                        if "".join(list(map(chr,lorawan.get_payload()))) == 'OK':
                            print("Transfer next data")
                            i = i + 1
                            break
                        else:
                            sleep(.5)
                            self.tx_counter = self.tx_counter+1
                            print("Retransmitting by wrong frame")
                            self.rx_packet = []
                            print("Retrying "+str(self.tx_counter)+" times")
                            frame = int("".join(list(map(chr,lorawan.get_payload()))))
                            i = frame
                            lorawan.create(MHDR.UNCONF_DATA_UP, {'devaddr': devaddr, 'fcnt': i, 'data': list(map(ord,data[i])) })
                            self.set_dio_mapping([1,0,0,0,0,0])
                            self.set_mode(MODE.STDBY)
                            self.write_payload(lorawan.to_raw())
                            self.set_mode(MODE.TX)
                            sleep(5)
                            BOARD.led_off()
                    else:
                        sleep(.5)
                        self.tx_counter = self.tx_counter+1
                        print("Retransmitting by not receiving")
                        print("Retrying "+str(self.tx_counter)+" times")
                        lorawan.create(MHDR.UNCONF_DATA_UP, {'devaddr': devaddr, 'fcnt': i, 'data': list(map(ord,data[i])) })
                        self.set_dio_mapping([1,0,0,0,0,0])
                        self.set_mode(MODE.STDBY)
                        self.write_payload(lorawan.to_raw())
                        self.set_mode(MODE.TX)
                        sleep(5)
                        BOARD.led_off()
                if self.tx_counter > 3:
                    print("Fail to send data,send again")
                    sleep(100)
            BOARD.led_off()
            self.set_mode(MODE.SLEEP)
            sleep(1000)

devaddr = [0xFF,0xFF, 0xFF, 0x00]
nwskey = [0xC3, 0x24, 0x64, 0x98, 0xDE, 0x56, 0x5D, 0x8C, 0x55, 0x88, 0x7C, 0x05, 0x86, 0xF9, 0x82, 0x26]
appskey = [0x15, 0xF6, 0xF4, 0xD4, 0x2A, 0x95, 0xB0, 0x97, 0x53, 0x27, 0xB7, 0xC1, 0x45, 0x6E, 0xC5, 0x45]
lora = LoRaSend()

lora.set_mode(MODE.SLEEP)
lora.set_dio_mapping([1,0,0,0,0,0])
lora.set_freq(915)
lora.set_pa_config(pa_select=1)
lora.set_spreading_factor(7)
lora.set_pa_config(max_power=0x0F, output_power=0x0E)
lora.set_sync_word(0x63)
lora.set_rx_crc(True)
lora.set_bw(BW.BW125)
lora.set_coding_rate(CODING_RATE.CR4_5)
lora.set_preamble(8)
print(lora)
lora.start()
