미래형 자동차 대회 아두이노 코드들

track -> 트랙에서 하는 주행

parking -> 주차 미션으로 공간 경우의 수가 두개이기 때문에 1과 2로 나눠서 작업

parking_misiion_1이 2번째 칸에 주차고, parking_mission_2가 3번째 칸에 주차하도록 작업함


<play>

아두이노 프로그램 업로드 후

<code>
rosrun rosserial_python serial_node.py _port:=/dev/ttyACM0 _baud:=57600
</code>  
  
manual 모드 실행시 추가로 실행해줘야되는 launch 파일
  
$ rosrun teleop_twist_keyboard teleop_twist_keyboard.py


