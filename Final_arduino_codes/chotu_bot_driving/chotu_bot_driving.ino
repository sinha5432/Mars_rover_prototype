 
int l1_dir1=24;
int l2_dir1=25;
int l3_dir1=23;
int r1_dir1=53;
int r2_dir1=45;
int r3_dir1=51;


int l1_pwm=5;
int r1_pwm=4;

int l2_pwm=7;
int r2_pwm=9;

int l3_pwm=6;
int r3_pwm=8;



void setup() {

  Serial.begin(9600);
  delay(50);
  Serial.setTimeout(500000);
  pinMode(l1_dir1,OUTPUT);
  pinMode(l2_dir1,OUTPUT);
  pinMode(l3_dir1,OUTPUT);
  
  
  pinMode(r1_dir1,OUTPUT);
  pinMode(r2_dir1,OUTPUT);
  pinMode(r3_dir1,OUTPUT);

  pinMode(l1_pwm,OUTPUT);
  pinMode(r1_pwm,OUTPUT);

  pinMode(l2_pwm,OUTPUT);
  pinMode(r2_pwm,OUTPUT);

  pinMode(l3_pwm,OUTPUT);
  pinMode(r3_pwm,OUTPUT);
}

void loop()
{

  
  int a,b;
  
  a=Serial.parseInt();  
  b=Serial.parseInt();

  if(a>=0) //Forward
  {
    digitalWrite(l1_dir1,LOW); 
    digitalWrite(l2_dir1,LOW);
    digitalWrite(l3_dir1,LOW);
        
    analogWrite(l1_pwm,a);
    analogWrite(l2_pwm,a);
    analogWrite(l3_pwm,a);
  }
  else //Backward
  {
    int a_1=(-1*a);
    digitalWrite(l1_dir1,HIGH); 
    digitalWrite(l2_dir1,HIGH);
    digitalWrite(l3_dir1,HIGH);
      
    analogWrite(l1_pwm,a_1);
    analogWrite(l2_pwm,a_1);
    analogWrite(l3_pwm,a_1);
  }
  if(b>=0) //Forward
  {
    
    digitalWrite(r1_dir1,LOW);
    digitalWrite(r2_dir1,LOW);
    digitalWrite(r3_dir1,LOW);
    analogWrite(r1_pwm,b);
    analogWrite(r2_pwm,b);
    analogWrite(r3_pwm,b);
  }
  else //Backward
  {
    int b_1=(-1*b);
    digitalWrite(r1_dir1,HIGH);
    digitalWrite(r2_dir1,HIGH);
    digitalWrite(r3_dir1,HIGH);
    
    
    analogWrite(r1_pwm,b_1);
    analogWrite(r2_pwm,b_1);
    analogWrite(r3_pwm,b_1);
  }
  
  
 }
