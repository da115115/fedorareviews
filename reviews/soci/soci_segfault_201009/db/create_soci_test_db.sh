#!/bin/sh

DB_NAME="soci_test"
DB_HOST="localhost"
DB_PORT="3306"

if [ "$1" != "" ]; then
	DB_NAME=$1
fi

if [ "$2" != "" ]; then
	DB_HOST=$2
fi 

if [ "$3" != "" ]; then
	DB_PORT=$3
fi


if [ "$1" = "--help" -o  "$1" = "-h" ]; then
	echo "Usage: $0 [ <Name of Database> <Host> <Port> ]"
	echo ""
	exit -1
fi

echo "Accessing mysql database hosted on $DB_HOST:$DB_PORT to create database '${DB_NAME}'. To create a database, username and password of an administrator-like MySQL account are required. On most of MySQL databases, the 'root' MySQL account has all the administrative rights, but you may want to use a less-privileged MySQL administrator account. Type the username of administrator followed by [Enter]. To discontinue, type ctrl-c."
read userinput_adminname

echo "Type $userinput_adminname's password followed by [Enter]"
read -s userinput_pw

SQL_STATEMENT="CREATE DATABASE IF NOT EXISTS ${DB_NAME} DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci"

echo "The database '${DB_NAME}' will be created:"
mysql -u ${userinput_adminname} --password=${userinput_pw} -P ${DB_PORT} -h ${DB_HOST} mysql -e "${SQL_STATEMENT}"

