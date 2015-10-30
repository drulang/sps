echo "Installing SPS-BE database"
echo "Enter MySQL db host"
read host

echo "Enter db username"
read username

echo "Setting up model"
mysql -u $username -p -h $host < ./db/sps-be-db-model.sql &&\
echo "Inserting base data" &&\
mysql -u $username -p -h $host < ./db/base.sql

echo "Finished"

