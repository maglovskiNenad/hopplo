Kako koristiti ovaj projekat:

1. Aktiviraj virtualno okruženje (/hopplo/hoplic_baksic):
   python3 -m venv venv && source venv/bin/activate

2. Instaliraj py2app:
   pip install py2app

3. Napravi .app:
   python setup.py py2app

4. Instaliraj create-dmg (ako već nisi):
   npm install -g create-dmg

5. Napravi .dmg fajl:
   ./create_dmg.sh
