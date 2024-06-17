import sys
from time import sleep
import json
from SX127x.LoRa import *
import LoRaWAN
from LoRaWAN.MHDR import MHDR
from SX127x.board_config import BOARD
from SX127x.constants import *
from MergeImage import *
BOARD.setup()

class LoRaGW(LoRa):
    def __init__(self, devaddr = [], nwkey = [], appkey = [], verbose=False):
        super(LoRaGW, self).__init__(verbose)
        self.devaddr=devaddr
        self.nwkey=nwkey
        self.appkey=appkey
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0,0,0,0,0,0])
        self.receive_frame = 0
        self.image_frame = []
    def on_tx_done(self):
        print("TxDone")
        self.set_dio_mapping([0,0,0,0,0,0])
        self.set_mode(MODE.STDBY)
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)
        self.clear_irq_flags(RxDone=1)
        BOARD.led_off()
    def on_rx_done(self):
        print("RxDone")
        self.clear_irq_flags(RxDone=1)
        lorawan = LoRaWAN.new(nwskey, appskey)
        payload = self.read_payload(nocheck=True)
        lorawan.read(payload)
        frame_number = int(''.join(f'{byte:02x}' for byte in (lorawan.get_mac_payload().get_fhdr().get_fcnt()[::-1])),16)
        print("Payload: ", lorawan.get_payload())
        print("Mac Version: ", lorawan.get_mhdr().get_mversion())
        print("Mac Type: ", lorawan.get_mhdr().get_mtype())
        print("Mic: ", lorawan.get_mic())
        print("Compute mic: ", lorawan.compute_mic())
        print("Check mic: ", lorawan.valid_mic())
        print("Dev Addr", lorawan.get_devaddr())
        print("Frame Number: ",frame_number)
        print("Data: ")
        print("".join(list(map(chr, lorawan.get_payload()))))
        sleep(1)
        self.reset_ptr_tx()
        if payload == None:
            self.set_mode(MODE.SLEEP)
            self.set_dio_mapping([1,0,0,0,0,0])    # TX
            sleep(.5)
            lora.set_pa_config(pa_select=1)
            self.set_mode(MODE.STDBY)
            sleep(.5)
            print("Send ACK")
            lorawan.create(MHDR.UNCONF_DATA_UP, {'devaddr': devaddr,'fcnt': 0, 'data': list(map(ord,'0')) })
            self.write_payload(lorawan.to_raw())
            self.set_mode(MODE.TX)
            print("Cannot Fetch Data")
        else:
            self.set_mode(MODE.SLEEP)
            self.set_dio_mapping([1,0,0,0,0,0])    # TX
            sleep(.5)
            lora.set_pa_config(pa_select=1)
            self.set_mode(MODE.STDBY)
            sleep(.5)
            self.clear_irq_flags(TxDone=1)
            print("\nSend ACK")
            if(sum(lorawan.mac_payload.fhdr.get_fcnt()) == 0):
                self.receive_frame = 0
            if(lorawan.get_devaddr()!=devaddr[::-1]):
                lorawan.create(MHDR.UNCONF_DATA_UP, {'devaddr': devaddr,'fcnt': 0, 'data': list(map(ord,'Ex')) })
                self.write_payload(lorawan.to_raw())
                print("Wrong node receive")
                self.set_mode(MODE.TX)
            elif(frame_number != self.receive_frame):
                lorawan.create(MHDR.UNCONF_DATA_UP, {'devaddr': devaddr,'fcnt': 0, 'data': list(map(ord,str(self.receive_frame)))})
                self.write_payload(lorawan.to_raw())
                print("Wrong data sequence")
                self.set_mode(MODE.TX)
            else: 
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
                lorawan.create(MHDR.UNCONF_DATA_UP, {'devaddr': devaddr,'fcnt': 0, 'data': list(map(ord,'OK'))})
                self.write_payload(lorawan.to_raw())
                print("Save Data Successful")
                self.receive_frame = self.receive_frame + 1
                print(self.read_payload())
                self.set_mode(MODE.TX)
    def start(self):
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)
        while True:
            BOARD.led_on()
            sleep(1)
            rssi_value = self.get_rssi_value()
            status = self.get_modem_status()
            sys.stdout.flush()
            sys.stdout.write("\r%d %d %d" % (rssi_value, status['rx_ongoing'], status['modem_clear']))
devaddr = [0xFF,0xFF, 0xFF, 0x00]
nwskey = [0xC3, 0x24, 0x64, 0x98, 0xDE, 0x56, 0x5D, 0x8C, 0x55, 0x88, 0x7C, 0x05, 0x86, 0xF9, 0x82, 0x26]
appskey = [0x15, 0xF6, 0xF4, 0xD4, 0x2A, 0x95, 0xB0, 0x97, 0x53, 0x27, 0xB7, 0xC1, 0x45, 0x6E, 0xC5, 0x45]
lora = LoRaGW(False)

lora.set_mode(MODE.SLEEP)
lora.set_dio_mapping([0,0,0,0,0,0])
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
