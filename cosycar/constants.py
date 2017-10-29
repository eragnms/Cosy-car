# -*- coding: utf-8 -*-

import os

class Constants():
    time_to_leave_file = '/tmp/cosycar_will_leave_at.txt'
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    config_file_name = '.config/cosycar.cfg'
    home_dir = os.environ['HOME']
    cfg_file = os.path.join(home_dir, config_file_name)
