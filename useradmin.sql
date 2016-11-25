CREATE USER 'admin'@'localhost' IDENTIFIED BY 'progettodin';

GRANT ALL PRIVILEGES ON ProgettoVM.* TO 'admin'@'localhost' WITH GRANT OPTION;

GRANT ALL ON test_ProgettoVM.* TO 'admin'@'localhost';
