[[ -d build/ ]] && rm -r build/ 
[[ -d build/ ]] && rm -r build/ 
[[ -d dist/ ]] && rm -r dist/
[[ -d cqls.egg-info/ ]] && rm -r cqls.egg-info/
python3 setup.py sdist bdist_wheel &&
twine upload dist/*
