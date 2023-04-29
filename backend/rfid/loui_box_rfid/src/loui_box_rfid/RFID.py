from abc import ABC, abstractmethod
from typing import List
from evdev import InputDevice, ecodes, InputEvent

class CardListener(ABC):

    @abstractmethod
    def card_read(self, card_id: str) -> None:
        pass


class KeyEventDecoder(ABC):

    @abstractmethod
    def convert_event(self, event: InputEvent) -> str:
        pass


class NumberKeyDecoder(KeyEventDecoder):

    def convert_event(self, event: InputEvent) -> str:
        if event.type != ecodes.EV_KEY  or event.value != 0:
            return ""
        
        if event.code == ecodes.KEY_0:
            return "0"
        if event.code == ecodes.KEY_1:
            return "1"
        if event.code == ecodes.KEY_2:
            return "2"
        if event.code == ecodes.KEY_3:
            return "3"
        if event.code == ecodes.KEY_4:
            return "4"
        if event.code == ecodes.KEY_5:
            return "5"
        if event.code == ecodes.KEY_6:
            return "6"
        if event.code == ecodes.KEY_7:
            return "7"
        if event.code == ecodes.KEY_8:
            return "8"
        if event.code == ecodes.KEY_9:
            return "9"
        
        return ""


class RFIDReader:

    device: InputDevice
    decoder: KeyEventDecoder
    listeners: List[CardListener]

    def __init__(self, devicePath: str) -> None:
        self.device = InputDevice(devicePath)
        self.listeners = []
        self.decoder = NumberKeyDecoder()

    def add_listener(self, listener: CardListener) -> None:
        self.listeners.append(listener)

    def run(self) -> None:
        self.device.grab()
        cardID: str = ""
        for event in self.device.read_loop():
            cardID += self.decoder.convert_event(event)
            if self.shall_notify(event):
                self.notify_listeners(cardID)
                cardID = ""


    def shall_notify(self, event: InputEvent) -> bool:
        return event.type == ecodes.EV_KEY \
            and event.value == 0 and event.code == ecodes.KEY_ENTER
        

    def notify_listeners(self, cardId: str) -> None:
        for listener in self.listeners:
            listener.card_read(cardId)

    def stop(self) -> None:
        self.device.ungrab()