NAVOD PRO SPUSTENI
------------------

1. vytvoreni virtualniho prostredi pro python
$ virtualenv venv

2. nastaveni pouziti pythonu 3
$ virtualenv -p /usr/bin/python3 venv

3. aktivace virtualniho prostredi
$ source venv/bin/activate

4. instalace pozadovanych knihoven
$ pip3 install -r requirements.txt

5. nastaveni udaju k databazi v souborech config.py a config_test.py

6a. spusteni webserveru
$ ./wish_api.py

6b. spusteni testu
$ ./test.py


REQUIREMENTS
------------
python3, pip3, virtualenv
