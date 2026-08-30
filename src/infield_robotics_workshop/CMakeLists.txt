cmake_minimum_required(VERSION 3.8)
project(infield_robotics_workshop)

find_package(ament_cmake REQUIRED)

install(PROGRAMS
  scripts/task1.py
  scripts/task2.py
  scripts/task3.py
  scripts/task4.py
  DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY
  data
  launch
  results
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
