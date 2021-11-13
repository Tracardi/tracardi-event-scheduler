python setup.py sdist bdist_wheel
python -m twine upload dist/*


rm -rf dist
rm -rf build
rm -rf tracardi_event_scheduler.egg-info
