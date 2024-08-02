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
* setting up phantomjs, there's a tree:
```bash
$ tree lists/static/tests/
lists/static/tests/
├── qunit-2.0.1.css
├── qunit-2.0.1.js
├── runner.js
└── tests.html

0 directories, 4 files
```
The text tells you how to get runner.js, but I don't know where the other ones came from.  I ended up checking out the book and taking them from there.  All I had was Spec.js there, and I think that was from a new section of the book, so did this change?

