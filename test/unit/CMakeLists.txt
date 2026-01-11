#    File:    CMakeLists.txt
#    Author:  Marvin Smith
#    Date:    7/8/2023
#

# Prepare for unit testing
terminus_test_prepare_unit()

#------------------------------------#
#-      Include Directories         -#
#------------------------------------#
include_directories( ${CMAKE_SOURCE_DIR}/library/include )
include_directories( ${CMAKE_BINARY_DIR}/library/include )

# Add unit tests
terminus_test_add_unit( all
    TEST_configure.cpp
    TEST_logger.cpp
    TEST_stream_interceptor.cpp
    TEST_utility.cpp
    TEST_json_formatter.cpp
    EXTRA_LIBS
        Boost::json
        Boost::log
        Boost::log_setup
        Boost::serialization
)