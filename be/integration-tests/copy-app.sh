
mkdir tmp 
cp -R $SPSHOME"/templates/" ./tmp/ 
cp -R $SPSHOME"/static/" ./tmp/
cp -R $SPSHOME"/lib/" ./tmp/lib/
cp $SPSHOME"/startdev.sh" ./tmp 
cp $SPSHOME"/sps-be.py" ./tmp
cp $SPSHOME"/integration-tests/sps.ini" ./tmp/sps.ini
cd tmp
ln -s $SPSHOME"/venv" ./venv
