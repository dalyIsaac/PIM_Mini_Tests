"""
Test harness for the PIM Mini.  
In order to choose what tests you want to run, set the appropriate Boolean values in `settings.py`
"""

from settings import STARTUP_TESTS, EEPROM_TESTS, FRAM_TESTS, RTC_TESTS, COMMS_TESTS,\
    LEDS_TESTS, USER_INPUTS_TESTS


def main():
    """Test harness"""
    if STARTUP_TESTS:
        from startup.startup import main as startup_main
        startup_main()
    if EEPROM_TESTS:
        # NOTE: Runs on PC
        from aardvark.eeprom import main as eeprom_main
        eeprom_main()
    if FRAM_TESTS:
        # NOTE: Runs on PC
        from aardvark.fram import main as fram_main
        fram_main()
    if RTC_TESTS:
        # NOTE: Runs on PC
        from aardvark.rtc import main as rtc_main
        rtc_main()
    if COMMS_TESTS:
        # NOTE: Runs on the PIM Mini
        from comms.comms import main as comms_main
        comms_main()
    if LEDS_TESTS:
        # NOTE: Runs on the PIM Mini
        from leds.leds import main as leds_main
        leds_main()
    if USER_INPUTS_TESTS:
        # NOTE: Runs on the PIM Mini
        from user_inputs.user_inputs import main as user_inputs_main
        user_inputs_main()

    print "\n\n\n"
    print " --- END OF TESTS --- "
    print "\n\n\n"


if __name__ == "__main__":
    main()
