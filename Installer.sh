#!/bin/sh

#  Installer.sh
#
#  This installer will ask the user for an installation directory. It will assume a default installation directory of usr/local/addborder/main.py.
#
#  Created by Arib Dhuka on 4/18/20.
#  

echo "Welcome to the addborder installer!"

echo "For default options press enter"

echo "Define installation directory [/usr/local/addborder]:"

read installationdir

if [ -z "$installationdir" ]
then
    actualdir="/usr/local/addborder"
else
    actualdir=$installationdir
fi

if [ ! -d "$actualdir" ]
then
    mkdir "$actualdir"
fi

if [ -e "$actualdir/main.py" ]
then
    rm "$actualdir/main.py"
fi

cp main.py "$actualdir/main.py"

FILENAME="addborder"
if [ -e $FILENAME ]
then
    rm $FILENAME
fi

echo "#!/bin/bash" > $FILENAME
echo "python3 $actualdir/main.py \$@" > $FILENAME
mv $FILENAME "/usr/local/bin/$FILENAME"
sudo chmod +x "/usr/local/bin/$FILENAME"
