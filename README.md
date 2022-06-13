
依赖
```
python -m pip install --user --upgrade setuptools wheel twine keyrings.cryptfile
```

打包库
```
python setup.py sdist bdist_wheel
```

上传到 pypi

```
twine upload dist/*
```