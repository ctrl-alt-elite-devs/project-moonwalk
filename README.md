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

![image](https://github.com/ctrl-alt-elite-devs/project-moonwalk/blob/main/static/images/logo.png)

This is the repository for Moonwalk Threads vintage clothing store website built with Django, showcasing a collection of curated, high-quality vintage apparel. The website provides an e-commerce platform where users can browse, view, and purchase unique, one-of-a-kind clothing items from various eras.

Features:
* Product Listings: A dynamic page displaying available clothing items, including details like size, price, and photos.
* Product Categories: Items are categorized by type (e.g., jackets, dresses, accessories) for easy browsing.
* Shopping Cart: Users can add products to their cart, view their selections, and proceed to checkout.
* User Authentication: Users can sign up, log in, and manage their accounts.
* Admin Panel: Admins can manage product listings, update stock, and handle orders through Django's built-in admin interface.
* Mobile-Friendly Design: The website is fully responsive, prioritizing mobile design first and expanding to desktop view.
* Integrated Payments: (Future feature) Integration with payment gateways for secure online transactions.

Technologies Used:
* Django: The backend framework for building and managing the website’s functionality.
* HTML/CSS/JavaScript: For the frontend design and interactivity.
* SQLite (or PostgreSQL/MySQL for production): Used for the database to store product and user information.

Ensure python is installed and added to PATH, then install all required modules by running:

    pip install -r requirements.txt

If new modules are needed add them manually to requirements.txt.

To run the server enter the following while in the main directory project-moonwalk:
  
    python manage.py runserver

Then proceed to http://127.0.0.1:8000/ to view output.

The moonwalk folder is the global settings for the entire project.

The myapp folder is the main application code for all of our pages.

The current html files within templates folder are all of the available pages
all of which extend the navbar created in base.html, anything added to this file will
appear on all pages that extend it.

# How to run on phone on your network

In settings.py add your local IP to the variable ALLOWED_HOSTS = [] 
example: ALLOWED_HOSTS = ['192.168.1.10', 'localhost', '127.0.0.1'] (replace 192.168.1.10 with your own local IP)

To find local IP

Windows use in cmd: 

    ipconfig
    
Look for the “IPv4 Address” under your active network connection (e.g., Wi-Fi or Ethernet). It should look like 192.168.1.10 or similar.

Mac in terminal:

    ipconfig getifaddr en0
    
will give you back your local ip

Run Django with the following command to make it accessible on your local network:

    python manage.py runserver 0.0.0.0:8000

Finally, on your phone's web browser enter:

    http://192.168.1.10:8000 (replace 192.168.1.10 with your own local IP)

now you should be able to see the page on your phone and be able to refresh and see updates as you change code.


# Git commands

Save progress to repo manually with git bash

    git add .

    git commit -m "your message"

    git push origin/main

If you have already set up the upstream

    git push

If using vscode use source control tool to handle git add/commit/push

In a terminal within your project directory run the following to update your local repo with changes on github repo:

    git fetch

Once local repo has been fully updated run the following to bring code from another branch into your current working branch:

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

# Software Images
![software-min](https://github.com/user-attachments/assets/484527e3-3f58-4b02-84dc-4e6f93c08576)

# Prototype
![figmaPrototype-min](https://github.com/user-attachments/assets/d35413ee-6d58-40a3-aadb-1eb9f3c363c8)

# Product
![demoWebsite-min](https://github.com/user-attachments/assets/83cc6900-0a6c-491a-bf6a-f1795368dede)

# ER Diagram

![image](https://github.com/user-attachments/assets/9735b085-cd8b-4829-a7fb-260fb5d25627)

# Testing
Tests located myapp/tests. Tests were done via Selenium and Chrome and Firefox web drivers. Run any of the test files in order to execute a test

# Deployment
The Moonwalk Threads website is deployed on an Ubuntu server hosted on AWS Lightsail. The production stack uses Gunicorn as the WSGI server and Nginx as a reverse proxy to serve the Django application.

Code updates are automatically triggered via a GitHub webhook connected to the main branch. When a new commit is pushed, the webhook notifies the server to update the project.

If needed, you can also manually pull and apply updates by following these steps:

1. SSH into the Server
    You can connect in two ways:
        -From your local terminal:
           `ssh -i your-key.pem ubuntu@your-server-ip`
        -Alternatively, use the built-in SSH terminal from the AWS Lightsail Console:
           -Go to your instance
           -Click "Connect using SSH"
   
2. Navigate to the Project Directory
   `cd ~/project_moonwalk/project-moonwalk`

3. Activate the Virtual Environment
   `source venv/bin/activate`

4. Pull the Latest Code from GitHub (Manual Method)
   `git pull origin main`
   
6. Install Dependencies
   `pip install -r requirements.txt`
   
7. Apply Database Migrations
   `python manage.py migrate`
   
8. Collect Static Files
   `python manage.py collectstatic`

9. Restart Gunicorn and Nginx
   `sudo systemctl restart gunicorn`
   `sudo systemctl restart nginx`

# SSL and HTTPS
Certbot is used to register SSL Certificate for our domain and is set to auto-renew the certificate annually.
To test that Certbot is properly setup to suto-renew still you can run the following command in a terminal connected to the server:
    `sudo certbot renew --dry-run`
