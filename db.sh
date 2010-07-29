export DJANGO_SETTINGS_MODULE="caco.settings"
export PYTHONPATH+="$PWD"

rm sad.sqlite3
python manage.py syncdb
#python parser-DAC.py
#python quest_batcher.py
#python disc_quest_attr.py
