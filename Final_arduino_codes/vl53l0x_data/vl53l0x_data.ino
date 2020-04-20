#include "Adafruit_VL53L0X.h"
#include <ros.h>
#include <std_msgs/Float64.h>



ros::NodeHandle  nh;
std_msgs::Float64 range;
ros::Publisher pub_range( "lidar", &range);


Adafruit_VL53L0X lox = Adafruit_VL53L0X();

void setup() {

  nh.getHardware()->setBaud(115200);
  nh.initNode();
  nh.advertise(pub_range);

  
  Serial.begin(115200);

  // wait until serial port opens for native USB devices
  while (! Serial) {
    delay(1);
  }
  
  Serial.println("Adafruit VL53L0X test");
  if (!lox.begin()) {
    Serial.println(F("Failed to boot VL53L0X"));
    while(1);
  }
  // power 
  Serial.println(F("VL53L0X API Simple Ranging example\n\n")); 
}


void loop() {
  VL53L0X_RangingMeasurementData_t measure;
    
  Serial.print("Reading a measurement... ");
  lox.rangingTest(&measure, false); // pass in 'true' to get debug data printout!

  if (measure.RangeStatus != 4) {  // phase failures have incorrect data

    if(measure.RangeMilliMeter>1500)
     {
      measure.RangeMilliMeter=65136;
     }
    Serial.print("Distance (mm): "); 
    Serial.println(measure.RangeMilliMeter);
    
    range.data=measure.RangeMilliMeter;
  } else {
    Serial.println(" out of range ");
    range.data=65136;
  }

  pub_range.publish(&range);
  nh.spinOnce();
  //delay(100);
}
