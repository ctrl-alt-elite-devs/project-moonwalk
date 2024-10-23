# project-moonwalk

Contributors:
* Ren Dhadda
* Sunshine Xiong
* Aye Myat Noe Khin
* Andrew Lawson
* Paul Arnett
* Julian Bucio
* Tyler Judt-Martine
* Nazar Potapchuk

Ensure python is installed and added to PATH, then in a terminal run:
    
    pip install django

To run the server enter the following while in the main directory project-moonwalk:
  
    python manage.py runserver

Then proceed to http://127.0.0.1:8000/ to view output.

The moonwalk folder is the global settings for the entire project.

The myapp folder is the main application code for all of our pages.

The current html files within templates folder are all of the available pages
all of which extend the navbar created in base.html, anything added to this file will
appear on all pages that extend it.

# Git commands

### Save progress to repo manually with git bash

    git add .

    git commit -m "your message"

    git push origin main

If you have already set up the upstream

    git push

If using vscode use source control tool to handle git add/commit/push

In a terminal within your project directory run the following to update your local repo with changes on github repo:

    git fetch

Once local repo has been fully updated run

    git merge origin/<branch-name>

### Warning

Avoid pushing to main/production until features are complete,
you should not be able to by default.
Avoid using -force commands as much as possible.

More questionable commands:

This command will override all your current changes and set your branch to desired branch:
Do not run this unless you want to lose all your work.

    git reset --hard origin/<branch-name>

Or if you want to undo changes already commited within your current branch you can run:

    git revert <commit-hash>

You can get the commit hashes from github's tracking system

