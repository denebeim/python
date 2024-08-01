* on jenkins global tools configuration.  It seems to be missing virtualenv.  I had to install it with apt.
* I couldn't figure out how to get virtualenv builder to work, I ended up using a shell instead, 
```bash
virtualenv .venv
. .venv/bin/activate
pip install -r requirements.txt
python src/manage.py test lists accounts
python src/manage.py test functional_tests
```
* I also needed to add selenium to the requirements.txt file.  Or continue reading the book since the other two problems were covered in it.  That's a me thing though, when a test fails I'll obsess over debugging it.
