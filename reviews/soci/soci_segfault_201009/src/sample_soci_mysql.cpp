// \see http://soci.sourceforge.net/doc/index.html
// STL
#include <iostream>
#include <istream>
#include <ostream>
#include <string>
#include <exception>
// SOCI
#include <soci/soci.h>
#include <soci/soci-mysql.h>

// ////////////////////// M A I N /////////////////////////
int main() {

  try {

    soci::session sql;
    std::string name;
    // int count = 0;
        
    sql.open("mysql", "db=soci_test user=soci password=soci");
    sql << "select name from categories where id = 4", soci::into(name);

    std::cout << "We have '" << name << "' entries in the categories."
              << std::endl;

  } catch (std::exception const& e) {
    std::cerr << "Error: " << e.what() << std::endl;
  }
}

