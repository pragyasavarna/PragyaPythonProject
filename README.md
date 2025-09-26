# Website :- Follow below steps to run this project
# Git and Python Install
git --version \
choco install gh \
refreshenv :- for refreshing the environment variable \
C:\Program Files\Git\bin :- add the path to git.exe in your PATH environment variable \
where anaconda \
C:\Users\pragya\anaconda3 :- add the path to python.exe in your PATH environment variable  \
python --version \
C:\Users\pragya\anaconda3\Scripts  :- add the path to pip.exe in your PATH environment variable \
pip --version

# Git Command
Github download \
https://git-scm.com/downloads \
Chocolatey  download \
@"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin" \
GitHub CLI (gh) download \
choco install gh \
gh auth login \
git config user.name "pragyasavarna" \
git config user.email "savarnapragya181751@gmail.com" \
git config user.email \
git config user.name \
git clone https://github.com/pragyasavarna/PragyaPythonProject.git \
git remote -v \
git init \
git status \
git add . \
git add filename \
git reset filename \
git config --global user.email "email_id" \
git config --global push.autoSetupRemote true \
git commit -m "First Commit" \
git push -u origin main \
git push -u origin \
git pull origin \
git fetch \
git stash \
git stash pop \
git switch main \

# Python Command
Run in Pycharm terminal for checking path of Python environment in Terminal \
python - c "import sys; print(sys.executable)" \
pip install -r requirements.txt \
For installing all python modules, run setup.py file \
pip install Django==4.2.4 \
python -m django --version \
django-admin startproject MyWebsite \
cd MyWebsite \
python manage.py startapp first_app \
python manage.py runserver \
python manage.py migrate \
python manage.py sqlmigrate first_app 0001 \
python manage.py makemigrations first_app \
python manage.py createsuperuser \

# Conda Command
conda info --envs \
conda create -n aiassistant python \
conda activate aiassistant \
https://github.com/UB-Mannheim/tesseract/wiki?utm_source=chatgpt.com
setx PATH "%PATH%;C:\Program Files\Tesseract-OCR" \
tesseract --version \
pip install pytesseract pyperclip pyttsx3 pyautogui vosk sounddevice \
conda deactivate \
conda env remove -n aiassistant \

# Admin Commands
To enable running scripts on the system \
In PowerShell as Administrator, run the following :- \ 
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted \
