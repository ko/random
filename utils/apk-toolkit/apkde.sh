#!/bin/sh

MYAPK=$1
MYAPK_WS="$MYAPK.ws/"
BIN_APKTOOL="/home/yaksok/bin/apktool"
BIN_DEX2JAR="/home/yaksok/bin/dex-translator-0.0.9.4/dex2jar.sh"
BIN_JAD="/home/yaksok/bin/jad"

echo "---------------------------------------------------------------"
echo "Creating new project workspace"
echo "---------------------------------------------------------------"
mkdir -vp $MYAPK_WS

echo "---------------------------------------------------------------"
echo "Decoding APK with apktool"
echo "---------------------------------------------------------------"
CALL_APKTOOL=`$BIN_APKTOOL d -f $MYAPK $MYAPK_WS/decoded`

echo "---------------------------------------------------------------"
echo "Coverting .dex to .jar"
echo "---------------------------------------------------------------"
CALL_DEX2JAR=`$BIN_DEX2JAR $MYAPK`

echo "---------------------------------------------------------------"
echo "Moving .jar files to workspace"
echo "---------------------------------------------------------------"
BASENAME=`echo $MYAPK | sed 's/.apk$//'`
JARNAME=${BASENAME}_dex2jar.jar
mv $JARNAME $MYAPK_WS/

echo "---------------------------------------------------------------"
echo "Moving to workspace directory"
echo "---------------------------------------------------------------"
cd $MYAPK_WS

echo "---------------------------------------------------------------"
echo "Converting .jar to .class"
echo "---------------------------------------------------------------"
unzip -d classes $JARNAME
pushd classes
for file in `find . -name '*.class'`; do
    $BIN_JAD -d $(dirname $file) -s java -lnc $file
done
popd

echo "---------------------------------------------------------------"
echo "Returning to working directory"
echo "---------------------------------------------------------------"
cd -


echo "---------------------------------------------------------------"
echo "Complete
echo "---------------------------------------------------------------"

