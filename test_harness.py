"""
Test harness for the PIM Mini.  
In order to choose what tests you want to run, set the appropriate Boolean values in `settings.py`
"""

from settings import STARTUP_TESTS, EEPROM_TESTS, FRAM_TESTS, ETHERNET_TESTS, USER_INPUTS_TESTS,\
    LEDS_TESTS, RTC_TESTS, ID_MODULE_TESTS, COMMS_TESTS, IO_EXTEND_COMMS_TESTS


def main():
    """Test harness"""
    if STARTUP_TESTS:
        pass
    if EEPROM_TESTS:
        from aardvark_tests.eeprom import main as eeprom_main
        eeprom_main()
    if FRAM_TESTS:
        from aardvark_tests.fram import main as fram_main
        fram_main()
    if ETHERNET_TESTS:
        pass
    if USER_INPUTS_TESTS:
        pass
    if LEDS_TESTS:
        pass
    if RTC_TESTS:
        from aardvark_tests.rtc import main as rtc_main
        rtc_main()
    if ID_MODULE_TESTS:
        pass
    if COMMS_TESTS:
        from comms_tests.comms import main as comms_main
        comms_main()
    if IO_EXTEND_COMMS_TESTS:
        pass

    print "\n\n\n"
    print " --- END OF TESTS --- "
    print "\n\n\n"

if __name__ == "__main__":
    main()
