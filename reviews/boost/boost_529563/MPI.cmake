# Copyright (C) Troy Straszheim
#
# Distributed under the Boost Software License, Version 1.0. 
# See accompanying file LICENSE_1_0.txt or copy at 
#   http://www.boost.org/LICENSE_1_0.txt 
#
set(MPI_FIND_QUIETLY TRUE)
find_package(MPI)

set(MPI_INCLUDE_PATH /usr/include/openmpi-x86_64)
set(MPI_COMPILE_FLAGS -I/usr/include/openmpi-x86_64)
set(MPI_LINK_FLAGS -L/usr/lib64/openmpi/lib -L/usr/lib64/openmpi/lib/openmpi -lmpi_cxx -lmpi)
set(MPI_LIBRARIES /usr/lib64/openmpi/lib/libmpi.so /usr/lib64/openmpi/lib/libmpi_cxx.so)

boost_external_report(MPI INCLUDE_PATH COMPILE_FLAGS LINK_FLAGS LIBRARIES)
  
