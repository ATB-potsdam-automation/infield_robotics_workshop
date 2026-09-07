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
from message_filters import ApproximateTimeSynchronizer, Subscriber
from rclpy.node import Node
from rclpy.parameter import Parameter
from sensor_msgs.msg import NavSatFix, RelativeHumidity


class RfidReader(Node):

    def __init__(self):
        super().__init__('listener')
        self.set_parameters([Parameter('use_sim_time', value=True)])

        self.declare_parameter('assumed_speed_mps', 2.0)
        self.declare_parameter('sync_queue_size', 10)
        self.declare_parameter('sync_slop_seconds', 0.3)

        self.assumed_speed_mps = self.get_parameter('assumed_speed_mps').value
        sync_queue_size = self.get_parameter('sync_queue_size').value
        sync_slop_seconds = self.get_parameter('sync_slop_seconds').value

        # initialise storage space for latest-value comparison
        self.current_pos = NavSatFix()

        # hook the first subscriber to our rfid-callback
        self.rfid_subscription = self.create_subscription(
            RelativeHumidity, "/rfid_detections", self.rfid_callback, 1
        )

        # hook the first subscriber to the fix-callback
        self.gps_subscription = self.create_subscription(
            NavSatFix, "/uav1/fix", self.gps_callback, 1
        )

        # set up a second set of subscribers for synchronized message handling
        self.synced_rfid_subscription = Subscriber(self, RelativeHumidity, "/rfid_detections")
        self.synced_gps_subscription = Subscriber(self, NavSatFix, "/uav1/fix")
        """
        YOUR CODE GOES Below this part:

        synchronize the RFID and GPS messages using the ApproximateTimeSynchronizer and log the detections using the synced_callback.
        class description:
        class ApproximateTimeSynchronizer(
            fs: list[Subscriber], # list of subscribers to synchronize
            queue_size: Unknown | None, # maximum number of messages to store for synchronization use sync_queue_size
            slop: Unknown | None, # maximum allowed time difference between messages use sync_slop_seconds
            allow_headerless: bool = False # whether to allow messages without headers 
            )
        Documentation can be found here: https://docs.ros.org/en/jazzy/p/message_filters/doc/Tutorials/Approximate-Synchronizer-Python.html            
        """
        
        # bool to avoid old latched message
        self.init = True

    def stamp_to_seconds(self, stamp):
        return stamp.sec + stamp.nanosec * 1e-9

    def log_detection(self, prefix, rfid_message: RelativeHumidity, gps_message: NavSatFix):
        rfid_time = self.stamp_to_seconds(rfid_message.header.stamp)
        gps_time = self.stamp_to_seconds(gps_message.header.stamp)
        delta_seconds = rfid_time - gps_time
        estimated_position_error_m = abs(delta_seconds) * self.assumed_speed_mps

        self.get_logger().info(
            f"{prefix} RFID-Sensor: {rfid_message.header.frame_id} "
            f"Humidity: {rfid_message.relative_humidity:f} "
            f"Lat: {gps_message.latitude:f} Long: {gps_message.longitude:f} "
            f"RFID time: {rfid_time:f} GPS time: {gps_time:f} "
            f"Delta: {delta_seconds:f} s "
            f"Estimated position error: {estimated_position_error_m:f} m"
        )

    # RFID detection callback
    def rfid_callback(self, message: RelativeHumidity):
        # skip first message (old latched)
        if self.init:
            return
        # use the most recent GPS position received by the node
        self.log_detection("latest GPS", message, self.current_pos)

    def synced_callback(self, rfid_message: RelativeHumidity, gps_message: NavSatFix):
        # use a GPS position selected by timestamp instead of callback order
        self.log_detection("synced GPS", rfid_message, gps_message)

    # GPS-position (fix) message callback
    def gps_callback(self, message: NavSatFix):

        # let other callbacks know that gps is available
        if self.init:
            self.init = False

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
