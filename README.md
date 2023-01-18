# wordcloudmaker
Générer un nuage de points à partir d'un pdf (pas nécessairement un cv d'ailleurs).  
Code écrit par Laurent Benaroya sous lisense GNU GPL v3.  
Note : cette version est adaptée aux documents en français.

## installation de pipenv
```bash
$ sudo apt install pipenv 
```
__OU__ si vous n'avez pas les doits administrateur (see https://pipenv.pypa.io/en/latest/install/)
```bash
$ pip install --user pipx
$ pip install --upgrade pip
$ pipx install pipenv
$ pip install --user pipenv
$ export PATH="/home/benaroya/.local/bin:$PATH"
```
Vous pouvez mettre export PATH dans votre ~/.bashrc  pour éviter d'avoir à le refaire à chaque fois que vous utilisez l'application.  
*Note : pipenv problem : https://github.com/pypa/pipenv/issues/5052*
## créer le projet
```bash
$ pipenv --python 3.8
$ pipenv install
$ pipenv shell
$ python -m textblob.download_corpora
```
## go for it !!!
génération du nuage de mots
```bash
$ pipenv shell
$ python wordcloudmaker.py --cv moncv.pdf --img monnuagedepoints.png --map Blues --lang french
```