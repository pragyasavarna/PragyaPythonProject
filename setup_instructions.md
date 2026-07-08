# Website :- Follow below steps to run this project

## Git and Python Install
* `git --version`
* `choco install gh`
* `refreshenv` :- for refreshing the environment variable 
* `C:\Program Files\Git\bin` :- add the path to git.exe in your PATH environment variable 
* `where anaconda`
* `C:\Users\pragya\anaconda3` :- add the path to python.exe in your PATH environment variable  
* `python --version`
* `C:\Users\pragya\anaconda3\Scripts` :- add the path to pip.exe in your PATH environment variable 
* `setx PATH "%PATH%;C:\Users\pragya\AppData\Roaming\Python\Python312\Scripts"` :- add the path in your PATH environment variable to remove script error 
* `pip --version`

## Git Commands

**Github download**
* https://git-scm.com/downloads
* https://git-lfs.com/

**Chocolatey download**
* `@"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"`

**GitHub CLI (gh) download**
* `choco install gh`
* `gh auth login`
* `git config user.name "pragyasavarna"`
* `git config user.email "savarnapragya181751@gmail.com"`
* `git config user.email`
* `git config user.name`
* `git clone https://github.com/pragyasavarna/PragyaPythonProject.git`
* `git remote -v`
* `git init`
* `git status`
* `git add .`
* `git add filename`
* `git reset filename`
* `git config --global user.email "email_id"`
* `git config --global push.autoSetupRemote true`
* `git commit -m "First Commit"`
* `git push -u origin main`
* `git push -u origin`
* `git pull origin`
* `git fetch`
* `git stash`
* `git stash pop`
* `git switch main`

**Git Deleted files Command**
* `for /f "delims=" %i in ('git ls-files --deleted') do git add "%i"`

**Set up Git LFS for your user account by running:**
* `git lfs install`
* `git lfs track "*.keras"`

**Undoes the git commit and unstage the files**
* `git reset HEAD~1`

## Python Commands

**Run in Pycharm terminal for checking path of Python environment in Terminal:**
* `python - c "import sys; print(sys.executable)"`

* `pip install -r requirements.txt`

**For installing all python modules, run setup.py file:**
* `pip install Django==4.2.4`
* `python -m django --version`
* `django-admin startproject MyWebsite`
* `cd MyWebsite`

**1. When creating a NEW Django app + NEW models**
* `python manage.py startapp first_app`
* `python manage.py makemigrations`
* `python manage.py migrate`
* `python manage.py createsuperuser`
* `python manage.py runserver`

**2. When making CHANGES to existing models**
* `python manage.py makemigrations`
* `python manage.py migrate`
* `python manage.py runserver`

**3. To SEE the SQL table in Django**
* `python manage.py sqlmigrate first_app 0001`

**4. Delete all data but keep tables**
* `python manage.py flush`

**5. DELETE ALL TABLES**
* **Step 1:** Delete the entire database file :- `del db.sqlite3`
* **Step 2:** Delete migration files :- 
  * `Get-ChildItem -Recurse -Include *.py -Path *\migrations | Where-Object { $_.Name -ne "__init__.py" } | Remove-Item`
* **Step 3:** Recreate database tables
  * `python manage.py makemigrations`
  * `python manage.py migrate`
  * `python manage.py createsuperuser`
  * `python manage.py runserver`

**6. To Run Django Server in Mobile also on LocalHost**
* `python manage.py runserver 0.0.0.0:8000`

## Conda Commands
* `conda info --envs`
* `conda create -n aiassistant python`
* `conda activate aiassistant`
* `conda install python=3.12.12`

**Tesseract OCR Install URL:**
* https://github.com/UB-Mannheim/tesseract/wiki?utm_source=chatgpt.com
* `setx PATH "%PATH%;C:\Program Files\Tesseract-OCR"`
* `tesseract --version`
* `pip install pytesseract pyperclip pyttsx3 pyautogui vosk sounddevice`
* `conda deactivate`
* `conda env remove -n aiassistant`

## Admin Commands
**To enable running scripts on the system, in PowerShell as Administrator, run the following:**
* `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted`

## Dataset Url
* https://www.kaggle.com/datasets/anthonytherrien/image-classification-64-classes-animal