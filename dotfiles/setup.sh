cpfile() {
    if [ "$1" == "$0" ]; then return; fi 
    ln -s $(pwd)/$1 ~
}

for f in *; do cpfile $f; done
for f in .*; do cpfile $f; done

grep "source ~/startup.sh" ~/.bashrc || echo "source ~/startup.sh" >> ~/.bashrc
