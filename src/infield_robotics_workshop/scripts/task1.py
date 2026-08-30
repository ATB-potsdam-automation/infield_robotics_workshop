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

        # bool to avoid old latched message
        self.init = True
        self.last_gps_log_time = None
   
    # RFID detection callback 
    def rfid_callback(self, message : RelativeHumidity):
        # skip first message (old latched)
        if self.init:
            return
        # print out the frame_id (in this case sensor_id) and the humidity value
        """
        YOUR CODE GOES BELOW THIS PART 
        
        add the latest GPS position to the data printout
        
        since variables are only valid within function scope (inside a function) we will use an object attribute that is set in the gps-callback
        
        object attributes can be accessed through "self.attribute" (e.g. print(self.init) )
        
        HINT: take a look at the printout in the gps-callback to get the syntax 
        
        """
        # print RFID-sensor info to the screen
        self.get_logger().info(
            f"Read RFID-Sensor! Sensor: {message.header.frame_id} "
            f"Humidity: {message.relative_humidity:f}"
        )
    
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
    
    
    
    
    
    
    
    
    
        
    
    
    
    