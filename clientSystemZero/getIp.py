'''
Use it incase of multiple IP's are visible
'''

import os
import subprocess
result = subprocess.run(['hostname', '-I'], capture_output=True, text=True)
output = result.stdout.strip()
myIp=output.split()
if len(myIp)==1:
    output=myIp[0]
else:
    output=myIp[0]

print(output)