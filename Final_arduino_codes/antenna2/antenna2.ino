/*
  HMC5883L Triple Axis Digital Compass. Compass Example.
  Read more: http://www.jarzebski.pl/arduino/czujniki-i-sensory/3-osiowy-magnetometr-hmc5883l.html
  GIT: https://github.com/jarzebski/Arduino-HMC5883L
  Web: http://www.jarzebski.pl
  (c) 2014 by Korneliusz Jarzebski
*/

#include <ros.h>
#include <Wire.h>
#include <HMC5883L.h>
#include <std_msgs/Float64.h>
#include <std_msgs/Int32.h>

#define pwm_pin 9
#define dir_pin_1 8
#define dir_pin_2 6



/* #define pwm_pin 3
 #define dir_pin_1 4
 #define dir_pin_2 5
*/

HMC5883L compass;

ros::NodeHandle  nh;
std_msgs::Float64 Float64;


void messageCb(const std_msgs::Int32& msg)
{
 int pwm_data= msg.data;
  
  if(pwm_data>0)
  {
    digitalWrite(dir_pin_1,HIGH);
    analogWrite(pwm_pin,pwm_data);
    digitalWrite(dir_pin_2,LOW);
    
  }
  else
  {
    int a=(-1)*pwm_data;
    digitalWrite(dir_pin_1,LOW);
    analogWrite(pwm_pin,a);
    digitalWrite(dir_pin_2,HIGH);
  }
}


ros::Publisher antenna_yaw( "/antenna_degree", &Float64);
ros::Subscriber<std_msgs::Int32> sub("/pwm", &messageCb);


void setup()
{

  pinMode(pwm_pin,OUTPUT);
  pinMode(dir_pin_1,OUTPUT);
  pinMode(dir_pin_2,OUTPUT);
  
  nh.getHardware()->setBaud(9600);
  nh.initNode();
  nh.advertise(antenna_yaw);
  nh.subscribe(sub);

  
  Serial.begin(9600);

  // Initialize Initialize HMC5883L
  //Serial.println("Initialize HMC5883L");
  while (!compass.begin())
  {
    //Serial.println("Could not find a valid HMC5883L sensor, check wiring!");
    delay(500);
  }

  // Set measurement range
  compass.setRange(HMC5883L_RANGE_1_3GA);

  // Set measurement mode
  compass.setMeasurementMode(HMC5883L_CONTINOUS);

  // Set data rate
  compass.setDataRate(HMC5883L_DATARATE_30HZ);

  // Set number of samples averaged
  compass.setSamples(HMC5883L_SAMPLES_8);

  // Set calibration offset. See HMC5883L_calibration.ino
  compass.setOffset(36,-133);
}

void loop()
{
  Vector norm = compass.readNormalize();

  // Calculate heading
  float heading = atan2(norm.YAxis, norm.XAxis);

  // Set declination angle on your location and fix heading
  // You can find your declination on: http://magnetic-declination.com/
  // (+) Positive or (-) for negative
  // For Bytom / Poland declination angle is 4'26E (positive)
  // Formula: (deg + (min / 60.0)) / (180 / M_PI);
  float declinationAngle = (4.0 + (26.0 / 60.0)) / (180 / M_PI);
  heading += declinationAngle;

  // Correct for heading < 0deg and heading > 360deg
  if (heading < 0)
  {
    heading += 2 * PI;
  }

  if (heading > 2 * PI)
  {
    heading -= 2 * PI;
  }

  // Convert to degrees
  float headingDegrees = heading * 180/M_PI; 

  //send to ROS
  Float64.data=headingDegrees;
  antenna_yaw.publish(&Float64);

  // Output
  Serial.print(" Heading = ");
  Serial.print(heading);
  Serial.print(" Degress = ");
  Serial.print(headingDegrees);
  Serial.println();

  nh.spinOnce();

 // delay(100);
}
