#include <iostream>
#include "boost/multi_array.hpp"

// Compile with:  g++ -I /home/minter/Downloads/Software/Boost/boost_1_75_0 -o dtr detrans.cpp
typedef boost::multi_array <double, 2> array_2d;

void detrans(array_2d &x_array,
	     array_2d &y_array,
	     size_t x_range,
	     size_t y_range,
	     double del_x,
	     double del_y) {
  
  // Corrects the effect of translation by removing the extent by which each point 
  // had been shifted, i.e. del_x, and del_y.
  
  for (auto i = 0; i < x_range; ++i) {
    for (auto j = 0; j < y_range; ++j) {
      x_array[i][j] = i-del_x;
      y_array[i][j] = j-del_y;
    }
  }

  std::cout << "Detrans was run" << std::endl;
}


int main() {

  size_t x_range = 4;
  size_t y_range = 3;
    
  array_2d x_in(boost::extents[4][3]);
  array_2d y_in(boost::extents[4][3]);
            

  double del_x = 0.1;
  double del_y = 0.2;
  
  detrans(x_in, y_in, x_range, y_range, del_x, del_y);

  for (auto i = 0; i < x_range; ++i) {
    for (auto j = 0; j < y_range; ++j) {
      std::cout << x_in[i][j] << ' ';
    }
    std::cout << '\n';
  }
  
  return 0;
}


