# -*- coding: utf-8 -*-

import os

class Constants():
    time_to_leave_file = '/tmp/cosycar_will_leave_at.txt'
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    cfg_file_path = '.config'
    cfg_file_name = 'cosycar.cfg'
    home_dir = os.environ['HOME']
    cfg_file = os.path.join(home_dir, cfg_file_path, cfg_file_name)
