# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 17:56:01 2022

@author: Edgar Tan
"""

import os
import certifi

os.environ['SSL_CERT_FILE'] = certifi.where() # ssl cert

# alternatively u can search environment variables from windows
# then go environment variables and add these default environment variables

