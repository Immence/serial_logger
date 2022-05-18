class Commands():
    """Contains all commands to be sent to fork"""

    @staticmethod
    def get_freq():
        """Retrieves the last measured frequency from the device"""
        return "fork get freq\n"
    
    @staticmethod
    def send_calibration_refrence():
        """Retrieves the last measured frequency from the device"""
        return "fork get calibration\n"

    @staticmethod
    def send_get_is_reference_fork():
        return "fork get is_reference_fork\n"

    @staticmethod
    def get_fork_constants():
        """Retrieves the last measured frequency from the device"""
        return "fork get constants\n"

    @staticmethod
    def get_cali_temp():
        return "fork get calitemp\n"

    @staticmethod
    def get_sg():
        return "fork get sg\n"

    @staticmethod
    def get_identity():
        return "info get identity oneline\n"

    @staticmethod
    def get_qr_code():
        return "info get qrcode\n"

    @staticmethod
    def get_hardware_id():
        return "info get hardware\n"

    @staticmethod
    def get_device_variant():
        return "info get variant\n"

    @staticmethod
    def get_temperature_c():
        return "temp get tempc\n"

    @staticmethod
    def get_temperature_f():
        return "temp get tempf\n"

    @staticmethod
    def get_temp_constants():
        return "temp get constants\n"

    @staticmethod
    def get_low_liquid_freq():
        return "fork get llfreq\n"

    @staticmethod
    def get_high_liquid_freq():
        return "fork get hlfreq\n"

    @staticmethod
    def get_liquid_freqs():
        return "fork get liquid freqs\n"

    @staticmethod
    def get_low_liquid_sg():
        return "sg get ll\n"

    @staticmethod
    def get_high_liquid_sg():
        return "sg get hl\n"

    @staticmethod
    def get_freq_read_n(n : int):
        return f"fork get freq read {n}"
    @staticmethod
    def get_freq_run():
        return "fork get freq run\n"

    @staticmethod
    def get_freq_stop():
        return "fork get freq stop\n"

    @staticmethod
    def set_low_liquid_sg(sg):
        return f"sg set ll {sg}\n"

    @staticmethod
    def set_high_liquid_sg(sg):
        return f"sg set hl {sg}\n"

    @staticmethod
    def set_low_liquid_freq():
        """Saves the frequency of the high density liquid to memory on the device"""
        return "fork set freq ll\n"

    @staticmethod
    def set_high_liquid_freq():
        """Saves the frequency of the high density liquid to memory on the device"""
        return "fork set freq hl\n"

    @staticmethod
    def set_fork_constant_a(constant):
        """Takes the A constant for the frequency to SG calculation and saves it to memory on the device"""
        return f"fork set constant a {constant}\n"

    @staticmethod
    def set_fork_constant_b(constant):
        """Takes the B constant for the frequency to SG calculation and saves it to memory on the device"""
        return f"fork set constant b {constant}\n"

    @staticmethod
    def set_cali_temp(temp):
        """Takes the calibration temperature and saves it to memory on the device"""
        return f"fork set calitemp {temp}\n"

    @staticmethod
    def set_qr_code(code):
        return f"info set qrcode {code}\n"

    @staticmethod
    def set_hardware_id(id):
        return f"info set hardware {id}\n"

    @staticmethod
    def set_device_variant(variant):
        return f"info set variant {variant}\n"

    @staticmethod
    def set_temp_constant_b(constant):
        return f"temp set constant b {constant}\n"

    @staticmethod
    def set_temp_constant_c(constant):
        return f"temp set constant c {constant}\n"

    @staticmethod
    def set_temp_constant_d(constant):
        return f"temp set constant d {constant}\n"

    @staticmethod
    def set_temp_constant_e(constant):
        return f"temp set constant e {constant}\n"

