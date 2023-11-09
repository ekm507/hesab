#!/bin/bash

echo "Welcome to hesab installer"

cd ~/.config
git clone https://github.com/ekm507/hesab.git
cd hesab
python3 -m venv .venv
source ~/.config/hesab/.venv/bin/activate
python -m pip install -r requirements.txt

cd ~/.local/bin/

echo "#!/bin/bash

source ~/.config/hesab/.venv/bin/activate

cd ~/.config/hesab/

./hesab" > hesab

echo "Installation done! you can use hesab by typing "hesab" into your terminal."