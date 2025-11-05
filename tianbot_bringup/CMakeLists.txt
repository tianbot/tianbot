cmake_minimum_required(VERSION 3.8)
project(tianbot_bringup)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)

string(ASCII 27 Esc)
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/env-hooks/99.my_tianbot.dsv.in")
  ament_environment_hooks("${CMAKE_CURRENT_SOURCE_DIR}/env-hooks/99.my_tianbot.dsv.in")
  message("--${Esc}[1;34m *** Add Customized Tianbot Environment Variables *** ${Esc}[0m")
else()
  ament_environment_hooks("${CMAKE_CURRENT_SOURCE_DIR}/env-hooks/99.default_tianbot.dsv.in")
  message("--${Esc}[1;33m *** Attention! Using default Tianbot Environment Variables *** ${Esc}[0m")
endif()

## Specify additional locations of header files
## Your package locations should be listed before other locations
install(DIRECTORY launch param
  DESTINATION share/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
