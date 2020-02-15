/*
  HMC5883L Triple Axis Digital Compass + MPU6050 (GY-86 / GY-87). Compass Example.
  Read more: http://www.jarzebski.pl/arduino/czujniki-i-sensory/3-osiowy-magnetometr-hmc5883l.html
  GIT: https://github.com/jarzebski/Arduino-HMC5883L
  Web: http://www.jarzebski.pl
  (c) 2014 by Korneliusz Jarzebski
*/


#include <ros.h>
#include <Wire.h>
#include <HMC5883L.h>
#include <MPU6050.h>
#include <std_msgs/Float64.h>
#include <ros/time.h>
#include <sensor_msgs/Range.h>




const int echoPin1 = 4;  //Echo pin
const int trigPin1 = 3;  //Trigger pin

const int echoPin2 = 43;
const int trigPin2 = 41;

const int echoPin3 = 6;
const int trigPin3 = 7;

const int echoPin4 = 33;
const int trigPin4 = 35;

const int echoPin5 = 27;
const int trigPin5 = 25;




const int maxRange = 400.0;   //Maximum range in centimeters
const int minRange = 0.0;     //Minimum range

unsigned long range_timer1;   
unsigned long range_timer2;
unsigned long range_timer3;
unsigned long range_timer4;
unsigned long range_timer5;   



ros::NodeHandle  nh;
std_msgs::Float64 Float64;
sensor_msgs::Range range_msg1;
sensor_msgs::Range range_msg2;
sensor_msgs::Range range_msg3;
sensor_msgs::Range range_msg4;
sensor_msgs::Range range_msg5;


HMC5883L compass;
MPU6050 mpu;


ros::Publisher imu_yaw( "/imu_degree", &Float64);
ros::Publisher pub_range1( "ultrasound1", &range_msg1);
ros::Publisher pub_range2( "ultrasound2", &range_msg2);
ros::Publisher pub_range3( "ultrasound3", &range_msg3);
ros::Publisher pub_range4( "ultrasound4", &range_msg4);
ros::Publisher pub_range5( "ultrasound5", &range_msg5);


float getRange1(){
    int sample1;      //Holds time in microseconds
    
    // Trigger pin goes low then high for 10 us then low
    //  to initiate the ultrasonic burst

    
    digitalWrite(trigPin1, LOW);
    
    delayMicroseconds(2);
    
    digitalWrite(trigPin1, HIGH);
   
    
    delayMicroseconds(10);
    digitalWrite(trigPin1, LOW);
   
    
    // read pulse length in microseconds on the Echo pin
    sample1 = pulseIn(echoPin1, HIGH);
   
    
    // sample in microseconds converted to centimeters
    // 343 m/s speed of sound;  time divided by 2
   // nh.spinOnce();
    return sample1/58.3;
    
}
float getRange2(){
    int sample2;      //Holds time in microseconds
    
    // Trigger pin goes low then high for 10 us then low
    //  to initiate the ultrasonic burst
    digitalWrite(trigPin2, LOW);
    
    delayMicroseconds(2);
    
    digitalWrite(trigPin2, HIGH);
   
    
    delayMicroseconds(10);
    digitalWrite(trigPin2, LOW);
   
    
    // read pulse length in microseconds on the Echo pin
    sample2 = pulseIn(echoPin2, HIGH);
   
    
    // sample in microseconds converted to centimeters
    // 343 m/s speed of sound;  time divided by 2
    //nh.spinOnce();
    return sample2/58.3;
}


float getRange3(){
    int sample3;      //Holds time in microseconds
    
    // Trigger pin goes low then high for 10 us then low
    //  to initiate the ultrasonic burst
    digitalWrite(trigPin3, LOW);
    
    delayMicroseconds(2);
    
    digitalWrite(trigPin3, HIGH);
   
    
    delayMicroseconds(10);
    digitalWrite(trigPin3, LOW);
   
    
    // read pulse length in microseconds on the Echo pin
    sample3 = pulseIn(echoPin3, HIGH);
   
    
    // sample in microseconds converted to centimeters
    // 343 m/s speed of sound;  time divided by 2
    //nh.spinOnce();
    return sample3/58.3;
}

float getRange4(){
    int sample4;      //Holds time in microseconds
    
    // Trigger pin goes low then high for 10 us then low
    //  to initiate the ultrasonic burst
    digitalWrite(trigPin4, LOW);
    
    delayMicroseconds(2);
    
    digitalWrite(trigPin4, HIGH);
   
    
    delayMicroseconds(10);
    digitalWrite(trigPin4, LOW);
   
    
    // read pulse length in microseconds on the Echo pin
    sample4 = pulseIn(echoPin4, HIGH);
   
    
    // sample in microseconds converted to centimeters
    // 343 m/s speed of sound;  time divided by 2
    //nh.spinOnce();
    return sample4/58.3;
}


float getRange5(){
    int sample5;      //Holds time in microseconds
    
    // Trigger pin goes low then high for 10 us then low
    //  to initiate the ultrasonic burst
    digitalWrite(trigPin5, LOW);
    
    delayMicroseconds(2);
    
    digitalWrite(trigPin5, HIGH);
   
    
    delayMicroseconds(10);
    digitalWrite(trigPin5, LOW);
   
    
    // read pulse length in microseconds on the Echo pin
    
    sample5 = pulseIn(echoPin5, HIGH);
   
    
    // sample in microseconds converted to centimeters
    // 343 m/s speed of sound;  time divided by 2
   // nh.spinOnce();
    return sample5/58.3;
}


char frameid1[] = "/ultrasound1";
char frameid2[] = "/ultrasound2";
char frameid3[] = "/ultrasound3";
char frameid4[] = "/ultrasound4";
char frameid5[] = "/ultrasound5";




void setup()
{
  nh.getHardware()->setBaud(9600);
  nh.initNode();
  nh.advertise(imu_yaw);
  nh.advertise(pub_range1);
  nh.advertise(pub_range2);
  nh.advertise(pub_range3);
  nh.advertise(pub_range4);
  nh.advertise(pub_range5);
  
  //Serial.begin(9600);

  // If you have GY-86 or GY-87 module.
  // To access HMC5883L you need to disable the I2C Master Mode and Sleep Mode, and enable I2C Bypass Mode

  while(!mpu.begin(MPU6050_SCALE_2000DPS, MPU6050_RANGE_2G))
  {
    //Serial.println("Could not find a valid MPU6050 sensor, check wiring!");
    delay(500);
    nh.spinOnce();
  }

  mpu.setI2CMasterModeEnabled(false);
  mpu.setI2CBypassEnabled(true) ;
  mpu.setSleepEnabled(false);


   // fill the description fields in the range_msg
  range_msg1.radiation_type = sensor_msgs::Range::ULTRASOUND;
  range_msg1.header.frame_id =  frameid1;
  range_msg1.field_of_view = 0.26;
  range_msg1.min_range = minRange;
  range_msg1.max_range = maxRange;

  range_msg2.radiation_type = sensor_msgs::Range::ULTRASOUND;
  range_msg2.header.frame_id =  frameid2;
  range_msg2.field_of_view = 0.26;
  range_msg2.min_range = minRange;
  range_msg2.max_range = maxRange;

  range_msg3.radiation_type = sensor_msgs::Range::ULTRASOUND;
  range_msg3.header.frame_id =  frameid2;
  range_msg3.field_of_view = 0.26;
  range_msg3.min_range = minRange;
  range_msg3.max_range = maxRange;

  range_msg4.radiation_type = sensor_msgs::Range::ULTRASOUND;
  range_msg4.header.frame_id =  frameid2;
  range_msg4.field_of_view = 0.26;
  range_msg4.min_range = minRange;
  range_msg4.max_range = maxRange;

  range_msg5.radiation_type = sensor_msgs::Range::ULTRASOUND;
  range_msg5.header.frame_id =  frameid2;
  range_msg5.field_of_view = 0.26;
  range_msg5.min_range = minRange;
  range_msg5.max_range = maxRange;


 
 
  
  // set the digita I/O pin modes
  pinMode(echoPin1, INPUT);
  pinMode(trigPin1, OUTPUT);

  pinMode(echoPin2, INPUT);
  pinMode(trigPin2, OUTPUT);

  pinMode(echoPin3, INPUT);
  pinMode(trigPin3, OUTPUT);

  pinMode(echoPin4, INPUT);
  pinMode(trigPin4, OUTPUT);

  pinMode(echoPin5, INPUT);
  pinMode(trigPin5, OUTPUT);



  // Initialize Initialize HMC5883L
  Serial.println("Initialize HMC5883L");
  while (!compass.begin())
  {
   // Serial.println("Could not find a valid HMC5883L sensor, check wiring!");
    delay(500);
    nh.spinOnce();
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
  compass.setOffset(85, -219); 
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
  Float64.data=headingDegrees;
  imu_yaw.publish(&Float64);


  // sample the range data from the ultrasound sensor and
  // publish the range value once every 50 milliseconds
  if ( (millis()-range_timer1) > 50){
    range_msg1.range = getRange1();
    range_msg1.header.stamp = nh.now();
    pub_range1.publish(&range_msg1);
    //nh.spinOnce();
    range_timer1 =  millis() + 50;
    
   }
  if ( (millis()-range_timer2) > 50){
    range_msg2.range = getRange2();
    range_msg2.header.stamp = nh.now();
    pub_range2.publish(&range_msg2);
    //nh.spinOnce();
    range_timer2 =  millis() + 50;
   }
  if ( (millis()-range_timer3) > 50){
  range_msg3.range = getRange3();
  range_msg3.header.stamp = nh.now();
  pub_range3.publish(&range_msg3);
  //nh.spinOnce();
  range_timer3 =  millis() + 50;
 }
  if ( (millis()-range_timer4) > 50){
    range_msg4.range = getRange4();
    range_msg4.header.stamp = nh.now();
    pub_range4.publish(&range_msg4);
    //nh.spinOnce();
    range_timer4 =  millis() + 50;
   }

    if ( (millis()-range_timer5) > 50){
    range_msg5.range = getRange5();
    range_msg5.header.stamp = nh.now();
    pub_range5.publish(&range_msg5);
    //nh.spinOnce();
    range_timer5 =  millis() + 50;
   }


 

  // Output
  /*Serial.print(" Heading = ");
  Serial.print(heading);
  Serial.print(" Degress = ");
  Serial.print(headingDegrees);
  Serial.println();*/

nh.spinOnce();
  //delay(100);
}
