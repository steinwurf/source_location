cmake_minimum_required(VERSION 3.10)
project(source_location)

find_package(Python COMPONENTS Interpreter)

# Use waf to resolve dependencies
if(NOT DEFINED STEINWURF_RESOLVE)
  message(STATUS "Resolving dependencies...")
  execute_process(
    COMMAND ${Python_EXECUTABLE} waf resolve ${STEINWURF_RESOLVE_OPTIONS}
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    RESULT_VARIABLE STATUS)

  if(STATUS AND NOT STATUS EQUAL 0)
    message(FATAL_ERROR "Failed: ${STATUS}")
  endif()

  set(STEINWURF_RESOLVE "${CMAKE_CURRENT_SOURCE_DIR}/resolve_symlinks")
  set(STEINWURF_TOP_NAME source_location)
endif()

# Define library
add_library(source_location INTERFACE)
target_compile_features(source_location INTERFACE cxx_std_11)

target_include_directories(source_location
  INTERFACE "${STEINWURF_RESOLVE}/source_location-source/include")

add_library(steinwurf::source_location ALIAS source_location)

# Install headers
install(
  DIRECTORY "${STEINWURF_RESOLVE}/source_location-source/include"
  DESTINATION ${CMAKE_INSTALL_PREFIX}/include
  FILES_MATCHING
  PATTERN *.hpp)

# Is top level project?
if(${CMAKE_PROJECT_NAME} STREQUAL ${PROJECT_NAME})
  # Build executables
  add_executable(format example/main.cpp)
  target_link_libraries(format source_location)
endif()
