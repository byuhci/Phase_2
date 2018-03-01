# beeper.py
from python_src import berry_api
from python_src import berry

# The Beeper has a single register (2).
# The upper nybble is the note, where 0x0 is C, going up by half steps to 0xB is B
# The lower nybble is the octave, with 0x0 being C3 (110 Hz).
# The simplest way to use this berry is to call the set_note method, passing in the
#   note as a string, which is used as a key in the notes dictionary to get the proper value.
# If you want to control the note and octave directly, you'll just need to use the
#   set_value method.
# You can go up as high as you want, but it will start to sound awful before 
#   leaving the human hearable range.
# ***IMPORTANT NOTE***: If you tell the beeper to play the same note it is already playing,
#  it will click.
class Beeper(berry.Berry):
    REG_NOTE = 2
    notes = {
        None:   0x00,
        "OFF":  0x00,
        "C3#":  0x10,
        "D3b":  0x10,
        "D3":   0x20,
        "D3#":  0x30,
        "E3b":  0x30,
        "E3":   0x40,
        "F3":   0x50,
        "F3#":  0x60,
        "G3b":  0x60,
        "G3":   0x70,
        "G3#":  0x80,
        "A3b":  0x80,
        "A3":   0x90,
        "A3#":  0xA0,
        "B3b":  0xA0,
        "B3":   0xB0,
        
        "C4":   0x01,
        "C4#":  0x11,
        "D4b":  0x11,
        "D4":   0x21,
        "D4#":  0x31,
        "E4b":  0x31,
        "E4":   0x41,
        "F4":   0x51,
        "F4#":  0x61,
        "G4b":  0x61,
        "G4":   0x71,
        "G4#":  0x81,
        "A4b":  0x81,
        "A4":   0x91,
        "A4#":  0xA1,
        "B4b":  0xA1,
        "B4":   0xB1,
        
        "C5":   0x02,
        "C5#":  0x12,
        "D5b":  0x12,
        "D5":   0x22,
        "D5#":  0x32,
        "E5b":  0x32,
        "E5":   0x42,
        "F5":   0x52,
        "F5#":  0x62,
        "G5b":  0x62,
        "G5":   0x72,
        "G5#":  0x82,
        "A5b":  0x82,
        "A5":   0x92,
        "A5#":  0xA2,
        "B5b":  0xA2,
        "B5":   0xB2,
        
        "C6":   0x03,
        "C6#":  0x13,
        "D6b":  0x13,
        "D6":   0x23,
        "D6#":  0x33,
        "E6b":  0x33,
        "E6":   0x43,
        "F6":   0x53,
        "F6#":  0x63,
        "G6b":  0x63,
        "G6":   0x73,
        "G6#":  0x83,
        "A6b":  0x83,
        "A6":   0x93,
        "A6#":  0xA3,
        "B6b":  0xA3,
        "B6":   0xB3,
        
        "C7":   0x04,
        "C7#":  0x14,
        "D7b":  0x14,
        "D7":   0x24,
        "D7#":  0x34,
        "E7b":  0x34,
        "E7":   0x44,
        "F7":   0x54,
        "F7#":  0x64,
        "G7b":  0x64,
        "G7":   0x74,
        "G7#":  0x84,
        "A7b":  0x84,
        "A7":   0x94,
        "A7#":  0xA4,
        "B7b":  0xA4,
        "B7":   0xB4,
        
        "C8":   0x05,
        "C8#":  0x15,
        "D8b":  0x15,
        "D8":   0x25,
        "D8#":  0x35,
        "E8b":  0x35,
        "E8":   0x45,
        "F8":   0x55,
        "F8#":  0x65,
        "G8b":  0x65,
        "G8":   0x75,
        "G8#":  0x85,
        "A8b":  0x85,
        "A8":   0x95,
        "A8#":  0xA5,
        "B8b":  0xA5,
        "B8":   0xB5
    }
    
    def __init__(self, name, address, berry_type):
        super().__init__(name, address, berry_type)
        self._note = "OFF"
        self.turn_off()
    
    @property
    def note(self):
        return self._note
    
    @note.setter
    def note(self, val):
        self.play_note(val)
    
    # note must be a valid key in the dictionary called notes
    # We support from C3 up to B6, where the keys are strings
    # If note is not a key in notes, print an error message and return
    def play_note(self, note):
        if not note in self.notes:
            berry_api.eprint("Error in set_note: note", note, "is not a valid note. %s" % self.to_string())
        else:
            value = self.notes[note]
            err = berry_api.set_device_multi_values(self.addr, self.REG_NOTE, [value], 1)
            if err != 0:
                berry_api.eprint("Error %d in set_note for %s" % (err, self.to_string()))
                self._note = None
            else:
                self._note = note
    
    # The upper nybble of value must be valid (in the range [0x0,0xB]), but otherwise
    # this method will simply write the desired value as the note.
    # This method does nothing if value is invalid.
    def set_value(self, value):
        if value < 0xC0:
            err = berry_api.set_device_multi_values(self.addr, self.REG_NOTE, [value], 1)
            if err != 0:
                berry_api.eprint("Error %d in turn_off. %s" % (err, self.to_string()))
        else:
            berry_api.eprint("Error in set_value: invalid value of 0x%x. %s" % (value, self.to_string()))

    def turn_off(self):
        err = berry_api.set_device_multi_values(self.addr, self.REG_NOTE, [0], 1)
        if err != 0:
            berry_api.eprint("Error %d in turn_off. %s" % (err, self.to_string()))
        self._note = "OFF"

### End class Beeper ###
