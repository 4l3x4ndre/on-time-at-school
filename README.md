# On time at school

Small web app to monitor french public transport API to know if there
is some disruption to train services, so you know if you will be late
at school.

It can respond with Json to be used with your raspberry or arduino.


```
apt-get install pyton3-venv python3-dev
python3 -venv myenv
source myenv/bin/activate
pip install -r requirements.txt
# if it fails on maya/pendulum :
# pip install -U setuptools

cp config.py.template config.py
vi config.py
```
