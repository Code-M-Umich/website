# Code-M Website
[code-m.eecs.umich.edu](code-m.eecs.umich.edu)

Still in development. Visit our production site [here](web.eecs.umich.edu/~cseschol).

# Contribute

## Getting Started

### Git
[Install Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
[Fork this repository](https://help.github.com/articles/fork-a-repo/)

### Python
[Install Python 2.7 on Windows](https://www.python.org/downloads/windows/)

For linux / unix systems
cd to the cloned directory
```
$ sudo pip install virtualenv
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt 
```

## Running the website
You will need to execute these commands everytime you work on the site
```
$ virtualenv venv
$ source venv/bin/activate
```
Once in the virutal environment, and root dir of the repo, run this command
```
$ python run.py
```
Then visit [http://localhost:5000/](http://localhost:5000/) in your browser.
