#!/usr/bin/env python3
# Copyright <2022> <Tjark Schuette (tschuette@atb-potsdam.de)>

# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

#     Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#     Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
#     Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, 
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, 
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, 
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from sensor_msgs.msg import RelativeHumidity, NavSatFix
import tf2_ros


class RfidReader(Node):

    def __init__(self):
        super().__init__('listener')
        self.set_parameters([Parameter('use_sim_time', value=True)])
        self.declare_parameter('humidity_threshold', 0.5)
        self.humidity_threshold = self.get_parameter('humidity_threshold').value

        # initialise storage space for 
        self.current_pos = NavSatFix()

        # hook the first subscriber to our rfid-callback
        self.create_subscription(RelativeHumidity, "/rfid_detections", self.rfid_callback, 1)

        # hook the first subscriber to the fix-callback
        self.create_subscription(NavSatFix, "/uav1/fix", self.gps_callback, 1)

        # set up a tf2 Buffer this stores the incoming tf-messages       
        self.tfBuffer = tf2_ros.Buffer()
        # set up our TransformListener, this gives us access to transformations (even past ones through the buffer)
        self.listener = tf2_ros.TransformListener(self.tfBuffer, self)

        # bool to avoid old latched message
        self.init = True
    
    def send_sensor_position_as_goal(self, timestamp):
        """
        YOUR CODE GOES HERE:
        
        Get the transform from the frame "map" to the frame "uav/base_link" (position of the uav) at the time of the measurement
        using the tfBuffer: self.tfBuffer.lookup_transform(target_frame, source_frame, time, timeout)
        
        Use the `timestamp` argument (the time the RFID message was recorded) as the lookup time,
        so the transform reflects the UAV position at the moment of detection instead of now.
        
        lookup_transform() will block until the transform between the two frames becomes available.
        Therefore, you can set a timeout with the 4. (optional) argument.
        
        (If you need more information regarding the time arguments look up the ROS function lookup_transform online)
        
        Translation [x y z] kann be accessed as e.g. transform_object.transform.translation.x ,
        equivalent rotation [x y z w] as e.g. transform_object.transform.rotation.x 
        
        Print out the resulting transformation as loginfo.

        Why don't we need to synchronize the GPS and RFID messages, here?
        """
        pass # do nothing
   
    # RFID detection callback 
    def rfid_callback(self, message : RelativeHumidity):
        # check if the humidity we read out is below threshold
        if message.relative_humidity < self.humidity_threshold:
            self.get_logger().info("Humidity too low: %.2f - Sending goal to UGV" % message.relative_humidity)
            # if it is below a certain threshold send the current UAV position as goal-point to the UGV
            self.send_sensor_position_as_goal(message.header.stamp)
        else:
            self.get_logger().info("Humidity acceptable: %.2f   - No action taken" % message.relative_humidity)
    
    # GPS-position (fix) message callback 
    def gps_callback(self, message : NavSatFix):
        
        # print the current position every two seconds (not for every message)
        self.get_logger().info(
            f"Read GPS Position. Lat: {message.latitude:f} Long: {message.longitude:f}",
            throttle_duration_sec=2.0,
        )
        
        # store the position in a object attribute
        self.current_pos = message     

    def run(self):

        # spin() simply keeps python from exiting until this node is stopped
        rclpy.spin(self)


def main(args=None):
    rclpy.init(args=args)
    rfid_reader = RfidReader()
    try:
        rfid_reader.run()
    except KeyboardInterrupt:
        # Ctrl+C requested shutdown.
        pass
    finally:
        rfid_reader.destroy_node()
    if rclpy.ok():
        rclpy.shutdown()


if __name__ == '__main__':
    main()