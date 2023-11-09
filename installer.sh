#!/bin/bash

echo "Welcome to hesab installer"

cd ~/.local/share
git clone https://github.com/ekm507/hesab.git
cd hesab
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt

cd ~/.local/bin/

echo "#!/bin/bash

source ~/.local/share/hesab/.venv/bin/activate

cd ~/.local/share/hesab/

./hesab "\$@"" > hesab
chmod +x hesab

echo "Installation done! you can use hesab by typing "hesab" into your terminal."