# Code-M Website
[code-m.eecs.umich.edu](https://code-m.eecs.umich.edu)

Still in development. Visit our production site [here](https://web.eecs.umich.edu/~cseschol).

# Contribute

## Getting Started

### Git
[Install Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

[Fork this repository](https://help.github.com/articles/fork-a-repo/)

### Python
[Install Python 2.7 on Windows](https://www.python.org/downloads/windows/)

For linux / unix systems
cd to the cloned directory
```bash
$ sudo pip install virtualenv
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt 
```
### Database


## Work on the Website
Open an issue on the original Code-M-Umich/webiste repo
Describe what you're going to be working on
In you're local repo, create a branch off of the development branch
```bash
git checkout -b myFeature development
```
Work on your feature/bux fix/etc
Your final commit (all done working) message should have "Fixes #<issue-number>" where <issue-number> is references the issue you opened on the repo.
Push your branch to Github and make a pull request, this command will push your changes to the Code-M-Umich/website repo
```bash
git push origin myFeature
```


## Running the website
You will need to execute these commands everytime you work on the site
```bash
$ virtualenv venv
$ source venv/bin/activate
```
Once in the virutal environment, and root dir of the repo, run this command
```bash
$ python run.py --development
```
You can specify a user by running the website with the -u option as follows
```bash
$ python run.py --development -u 'myuniqname'
```
You can visit the site [http://localhost:5000/](http://localhost:5000/) in your browser.


## Troubleshooting
If you run the app and get the error
`OperationalError: (2003, "Can't connect to MySQL server on 'localhost' ([Errno 111] Connection refused)")`
Find your mysql socket path by runing the following command
`$ mysqladmin | grep socket`
Take the path from the output and run the app as follows
```bash
$ python run.py --development -s '<path>'
```