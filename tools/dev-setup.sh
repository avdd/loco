#!/bin/bash -eu

export PATH=$PATH:$HOME/.local/bin

here=$(dirname $(readlink -f $0))
top=$(dirname $here)
cd $top

$here/install-geckodriver.sh
pip install -r ./python-requirements.txt
python_user_site=$(python -m site --user-site)
echo $top/src > $python_user_site/loco.pth
. $NVM_DIR/nvm.sh
nvm install --lts
npm install
