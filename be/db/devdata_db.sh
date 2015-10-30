echo "Installing dev data"
echo "Enter MySQL db host"
read host

echo "Enter db username"
read username

echo "Setting up model"
mysql -u $username -p -h $host < ./db/dev-data.sql

echo "Finished"

