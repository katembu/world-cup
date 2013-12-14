INSERT INTO world_cup.user_management_customuser (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
SELECT id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined
FROM world_cup.auth_user
