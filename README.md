You'll  need to rename config.ini.sample to the config.ini and change data there if needed but also dont forget to change sqlalchemy.url in the alembic.ini

Here you can see the files, for db creation if needed.
Alembic files to create tables.
File to fill it with fake data with the help of a seed file.
Files with SQL queries named my_select.py.
And main file where you can make queries from the command prompt using the argparse module.
If you want to pass parameters through the cmd, you'll need to use next parameters:
--a - action
--m - model
--n - name
--id - id
--mark - mark
--t_id'- tutor_id
--sub_id - subject_id
--s_id - student_id
--g_id - group_id
But also feel free to check the files, there can be some useful commands