world-cup
=========

Django based web-application designed to allow users to predict the World Cup matches and create competitive groups with their friends.

Installation
-------------
1. Clone repository
2. Create MySQL schema named ``world_cup``
3. Change directory into the ``world-cup/world_cup/`` folder.
4. Run the command ``pip install -r requirements.txt``
5. Run the command ``python manage.py syncdb``
6. Run the command ``mysql -u root world_cup < tournament_countries.sql``
7. You'll need to create matches for the admin user created on database creation.
8. Run ``python manage.py shell``
9. ``from django.contrib.auth.models import User``
10. ``from tournament.helpers import create_matches``
11. ``user = User.objects.get(id=1)``
12. ``create_matches(user)``
13. Close the shell
14. Run the server with ``python manage.py runserver``
