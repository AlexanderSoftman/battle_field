setup and run application:
--------------------------
``` bash
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt 
python setup.py install
battle_field
```

``` python
def find_enemies(self):
    # 1. find all colliding with vision items
    items_in_vision = self.scene().collidingItems(self.vision)
    print("%s count items_in_vision" % (
        items_in_vision,))
    if len(items_in_vision) == 0:
```