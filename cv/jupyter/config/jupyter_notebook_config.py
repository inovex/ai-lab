import os
from IPython.lib import passwd

c.NotebookApp.ip = '0.0.0.0'
c.NotebookApp.port = 8888
c.NotebookApp.open_browser = False
c.MultiKernelManager.default_kernel_name = 'python3'

# Disable authentication
# Make sure to remove this in a non dev-only environment.
c.NotebookApp.token = ''
c.NotebookApp.password = ''
