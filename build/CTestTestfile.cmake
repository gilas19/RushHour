# CMake generated Testfile for 
# Source directory: /cs/usr/ticher/Downloads/RushHour
# Build directory: /cs/usr/ticher/Downloads/RushHour/build
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(unit_tests "/cs/usr/ticher/Downloads/RushHour/build/tests")
set_tests_properties(unit_tests PROPERTIES  _BACKTRACE_TRIPLES "/cs/usr/ticher/Downloads/RushHour/CMakeLists.txt;52;add_test;/cs/usr/ticher/Downloads/RushHour/CMakeLists.txt;0;")
subdirs("_deps/googletest-build")
