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
from geometry_msgs.msg import PoseStamped
from rclpy.duration import Duration
from rclpy.node import Node
from rclpy.parameter import Parameter
from sensor_msgs.msg import RelativeHumidity, NavSatFix
import tf2_ros
import tf_transformations
import tf2_geometry_msgs


class RfidReader(Node):

    def __init__(self):
        super().__init__('listener')
        self.set_parameters([Parameter('use_sim_time', value=True)])

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
        self.last_gps_log_time = None
    
    def send_current_position_as_goal(self):

        # get the transform
        try:
            transform = self.tfBuffer.lookup_transform(
                "uav/base_link", "map", self.get_clock().now(), timeout=Duration(seconds=0.1)
            )
        except tf2_ros.TransformException as error:
            self.get_logger().warning(f"Could not transform map to uav/base_link: {error}")
            return
        # print out the rotation
        self.get_logger().info(
            "received Rotation: (%f, %f, %f, %f)" % (
                transform.transform.rotation.x,
                transform.transform.rotation.y,
                transform.transform.rotation.z,
                transform.transform.rotation.w,
            )
        )
        # print out the translation
        self.get_logger().info(
            "received Translation: (%f, %f, %f)" % (
                transform.transform.translation.x,
                transform.transform.translation.y,
                transform.transform.translation.z,
            )
        )
        """
        YOUR CODE GOES HERE:
        
        apply the transform to the current position of the UAV on the ground.
        
        Reminder: p' = q * p * conj(q) 
        
        Or use the utility function for transformation provided by the tfBUffer class
         - best: do both and compare the results
        
        """
    
    # RFID detection callback 
    def rfid_callback(self, message : RelativeHumidity):
        # skip message if no gps-data is available yet
        if self.init:
            return
        # check if the humidity we read out is below threshold
        if message.relative_humidity < 0.5:
            self.get_logger().info("Humidity too low - Sending goal to UGV")
            # if it is below a certain threshold send the current UAV position as goal-point to the UGV
            self.send_current_position_as_goal()      
    
    # GPS-position (fix) message callback 
    def gps_callback(self, message : NavSatFix):
        
        # let other callbacks know that gps is available
        if self.init:
            self.init = False
        
        # print the current position every two seconds (not for every message)
        now = self.get_clock().now()
        if self.last_gps_log_time is None or (now - self.last_gps_log_time).nanoseconds >= 2_000_000_000:
            self.get_logger().info(
                f"Read GPS Position. Lat: {message.latitude:f} Long: {message.longitude:f}"
            )
            self.last_gps_log_time = now
        
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