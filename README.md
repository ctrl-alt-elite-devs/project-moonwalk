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
  `pip install django`

To run the server enter the following while in the main directory project-moonwalk:
  `python manage.py runserver`

Then proceed to http://127.0.0.1:8000/ to view output.

The moonwalk folder is the global settings for the entire project.

The myapp folder is the main application code for all of our pages.

The current html files within templates folder are all of the available pages
all of which extend the navbar created in base.html, anything added to this file will
appear on all pages that extend it.
