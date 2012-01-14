
# Compilation flags
CC = g++
CXXFLAGS = -Wall -fPIC -DSOCI_HEADERS_BURIED -DSOCI_MYSQL_HEADERS_BURIED
LDFLAGS = -lsoci_core -lsoci_mysql -L/usr/lib/mysql -lmysqlclient_r

# User-defined
SRC = sample_soci_mysql.cpp
OBJ = ${SRC:.cpp=.o}
EXEC = sample_soci_mysql

# Targets
all: $(EXEC)

.cpp.o: $(SRC)
	$(CC) $(CXXFLAGS) -c $< -o $@

sample_segfault: $(OBJ)
	$(CC) $(LDFLAGS) $< -o $(EXEC)

clean:
	rm -f $(EXEC) *.o *~
