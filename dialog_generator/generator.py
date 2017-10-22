# -*- coding: utf-8 -*-
import sys
import subprocess

def generate_dialog(genre='comedy', rating_level='high'):
    result = subprocess.check_output([
            sys.executable, 
            'char_rnn_tensorflow_master/sample.py',
            '--save_dir=char_rnn_tensorflow_master/save/' + genre + '_' + rating_level
            ]).decode().replace('\\r\\n', '\n').replace('\\t', '\t').replace('b', '').replace('"', '').strip()
    
    return result
