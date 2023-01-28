drive control -> autonomous mode

keyboard -> manual

->keyboard mode 사용시 설치 필요한 패키지

<teleop_key>

$ sudo apt-get install ros-noetic-teleop-twist-keyboard   또는   
$ sudo apt-get install ros-melodic-teleop-twist-keyboard



<play>
아두이노 프로그램 업로드 후


$ rosrun rosserial_python serial_node.py _port:=/dev/ttyACM0 _baud:=57600

