# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 10:28:14 2021

@author: jesal
"""

"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd
df = pd.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 40]
})

df