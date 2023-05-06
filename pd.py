import requests
from datetime import datetime
import sys

format = '%Y-%m-%d %H:%M:%S'
time = requests.get('http://worldtimeapi.org/api/timezone/Europe/Moscow').json()['datetime'].split('.')[0].replace('T',' ')
if datetime.strptime('2023-05-08 0:00:00', format) < datetime.strptime(time, format):
    print('ГОНИ ДЕНЬГИ :0')
    input('...')
    sys.exit(1)
print('TRIAL: ',datetime.strptime('2023-05-08 0:42:07', format) - datetime.strptime(time, format))