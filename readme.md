gmopg
===

GMOペイメントゲートウェイにプロトコルタイプで接続する為のPythonライブラリ

# Install

```
sudo pip install gmopg
```

# Uninstall
```
sudo pip uninstall gmopg
```

# Test
```
sudo pip install pytest
py.test ./tests
```

```
sudo pip install pytest-cov
py.test --cov=gmopg ./tests
```

# Usage

ExecTran.idPassをコールするサンプル

```python
from gmopg import GMOPG

gmopg = GMOPG(timeout=10, production=True)
try:
  response = gmopg.tran.execute({'ShopID': 'your-shop-id', 'ShopPass': 'your-shop-pass', 'OrderID': 'your-order-id': '1234', 'JobCD': '1234'})
except ResponseError as e:
  print(e)
else:
  print(response.data)
```

パラメタ名はペイメントゲートウェイの仕様書準拠です。 
