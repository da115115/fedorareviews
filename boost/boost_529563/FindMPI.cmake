# Finds the Message Passing Interface (MPI) Library
#
#  MPI_FOUND          - True if MPI found.
#  MPI_CXX_FOUND      - True if MPI's internationalization library found.
#  MPI_INCLUDE_PATHS   - Directory to include to get MPI headers
#                       Note: always include MPI headers as, e.g., mpi.h
#  MPI_LIBRARIES      - Libraries to link against for the common MPI
#  MPI_CXX_LIBRARIES  - Libraries to link against for MPI C++
#                       (note: in addition to MPI_LIBRARIES)
#
# Denis Arnaud (Dec. 2009)

# Look for the header file.
find_path(
  MPI_INCLUDE_PATH 
  NAMES mpi.h
  DOC "Include directory for the MPI library")
mark_as_advanced(MPI_INCLUDE_PATH)

# Look for the library.
find_library(
  MPI_LIBRARY
  NAMES mpi
  DOC "Libraries to link against for the common parts of MPI")
mark_as_advanced(MPI_LIBRARY)

# Copy the results to the output variables.
if(MPI_INCLUDE_PATH AND MPI_LIBRARY)
  set(MPI_FOUND 1)
  set(MPI_LIBRARIES ${MPI_LIBRARY})
  set(MPI_INCLUDE_PATHS ${MPI_INCLUDE_PATH})

  # Look for the MPI C++ libraries
  find_library(
    MPI_CXX_LIBRARY
    NAMES mpi_cxx
    DOC "Libraries to link against for MPI C++")
  mark_as_advanced(MPI_CXX_LIBRARY)
  if (MPI_CXX_LIBRARY)
    set(MPI_CXX_FOUND 1)
    set(MPI_CXX_LIBRARIES ${MPI_CXX_LIBRARY})
  else (MPI_CXX_LIBRARY)
    set(MPI_CXX_FOUND 0)
    set(MPI_CXX_LIBRARIES)
  endif (MPI_CXX_LIBRARY)
else(MPI_INCLUDE_PATH AND MPI_LIBRARY)
  set(MPI_FOUND 0)
  set(MPI_CXX_FOUND 0)
  set(MPI_LIBRARIES)
  set(MPI_CXX_LIBRARIES)
  set(MPI_INCLUDE_PATHS)
endif(MPI_INCLUDE_PATH AND MPI_LIBRARY)
