import os
from datetime import datetime

docker_version = '1.1'
print('===========================================================================================')
print('docker_version : ' + docker_version)
print('===========================================================================================')

os.system(f'docker build -t modoobattle:{docker_version} C:/Users/PC/Desktop/modoobattle_server/.')

os.system(f'docker save -o C:/Users/PC/Desktop/docker_image/modoobattle_{docker_version}.tar modoobattle:{docker_version}')

print('finish docker_version : ' + docker_version)

