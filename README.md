# psychic

Buzzfeed style predictive quizzes

### Installation:

1. Install Python 3

```bash
sudo apt-get install python3 python3-pip
```

2. Set up a virtual environment, I use `virtualenv`

```bash
sudo python3 -m pip install virtualenv
mkdir ~/.envs
python3 -m virtualenv ~/.envs/psychic
```

3. Install the dependencies in the virtualenv using pip 

```bash
source ~/.envs/psychic/bin/activate
pip install -r requirements.txt
```

4. Run the dev server

```bash
cd psychic
./manage.py runserver
```

5. Open `localhost:8000` in a web browser

### Changes to make for deployment

1. `settings.py`
    - Set `DEBUG` to False
    - Set `ALLOWED_HOSTS`
2. `~/.bashrc`
    - Add `export SECRET_KEY="(insert secret key here)"`

