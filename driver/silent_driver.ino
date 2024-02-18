#include <TMCStepper.h> 
#include <SoftwareSerial.h> 

// Define the common stepper motor pins 
#define EN_PIN_1          13 
#define EN_PIN_2          10 
#define DIR_PIN_1         11
#define STEP_PIN_1        12 
#define DIR_PIN_2         8 
#define STEP_PIN_2        9 
#define SW_RX             5 
#define SW_TX             4 
#define SW2_RX            3 
#define SW2_TX            2


#define R_SENSE           0.11f  // Adjust based on your driver 
#define DRIVER_ADDRESS    0b00   // TMC2209 default address 
//#define SERIAL_PORT       Serial 

SoftwareSerial SoftSerial(SW_RX, SW_TX); 
SoftwareSerial SoftSerial1(SW2_RX, SW2_TX); 
TMC2209Stepper driver(&SoftSerial, R_SENSE, DRIVER_ADDRESS); // Software serial 
TMC2209Stepper driver1(&SoftSerial1, R_SENSE, DRIVER_ADDRESS); 

const float stepSize = (3.0 / 50.0) * PI; // mm 
long int microsteps = 16; 
int steps = 16; 

// Variables to keep track of position and movement 
float current_X = 0.0; 
float current_Y = 0.0; 
float target_X = 0.0; 
float target_Y = 0.0; 
int move_X = 0; 
int move_Y = 0; 

float voltage;

struct Coordinate {
    int x;
    int y;
};

void gen(int x, int y, Coordinate* result) {
    Coordinate temp[] = {
        {x, y}, {x + 1, y}, {x + 1, y + 1}, {x, y + 1}, 
        {x - 1, y + 1}, {x - 1, y}, {x - 1, y - 1}, {x, y - 1}, 
        {x + 1, y - 1},

        {x+2, y-1}, {x+2,y}, {x+2,y+1}, {x+2,y+2},
        {x+1,y+2}, {x, y+2}, {x-1, y+2}, {x-2,y+2},
        {x-2,y+1},{x-2,y},{x-2,y-1},{x-2,y-2},
        {x-1,y-2},{x,y-2},{x+1,y-2},{x+2,y-2},

        {x+3,y-2},{x+3,y-1},{x+3,y},{x+3,y+1},{x+3,y+2},{x+3,y+3},
        {x+2,y+3},{x+1,y+3},{x,y+3},{x-1,y+3},{x-2,y+3},{x-3,y+3},
        {x-3,y+2},{x-3,y+1},{x-3,y},{x-3,y-1},{x-3,y-2},{x-3,y-3},
        {x-2,y-3},{x-1,y-3},{x,y-3},{x+1,y-3},{x+2,y-3},{x+3,y-3},

        {x+4,y-3},{x+4,y-2},{x+4,y-1},{x+4,y},{x+4,y+1},{x+4,y+2},{x+4,y+3},{x+4,y+4},
        {x+3,y+4},{x+2,y+4},{x+1,y+4},{x,y+4},{x-1,y+4},{x-2,y+4},{x-3,y+4},{x-4,y+4},
        {x-4,y+3},{x-4,y+2},{x-4,y+1},{x-4,y},{x-4,y-1},{x-4,y-2},{x-4,y-3},{x-4,y-4},
        {x-3,y-4},{x-2,y-4},{x-1,y-4},{x,y-4},{x+1,y-4},{x+2,y-4},{x+3,y-4},{x+4,y-4}
    };

    for (int i = 0; i < 81; ++i) {
        result[i] = temp[i];
    }
}

const int analogPin = A0; 

void setup() { 

  pinMode(EN_PIN_1,OUTPUT); 
  pinMode(EN_PIN_2,OUTPUT); 
  pinMode(STEP_PIN_1,OUTPUT); 
  pinMode(STEP_PIN_2,OUTPUT); 
  pinMode(DIR_PIN_1,OUTPUT); 
  pinMode(DIR_PIN_2,OUTPUT); 
  digitalWrite(EN_PIN_1,LOW); 
  digitalWrite(EN_PIN_2,LOW); 


  Serial.begin(115200); 
  SoftSerial.begin(115200); 
  //SoftSerial1.begin(115200); 
  //driver.beginSerial(115200); 
  //Serial.begin(115200); 
   
 
  // TMC2209Stepper Initialization 
  driver.begin(); 
  driver.intpol(1); 
  driver.TCOOLTHRS(0xFFFFF); 
  driver.rms_current(1700); 
  //driver.en_pwm_mode(1); 
  driver.pwm_autoscale(1); 
  driver.en_spreadCycle(0); 
  driver.microsteps(microsteps);  // Set microstepping mode to 1/16 

  SoftSerial.end();

  SoftSerial1.begin(115200);
  driver1.begin(); 
  driver1.intpol(1); 
  driver1.TCOOLTHRS(0xFFFFF); 
  driver1.rms_current(1700); 
  //driver.en_pwm_mode(1); 
  driver1.pwm_autoscale(1); 
  driver1.en_spreadCycle(0); 
  driver1.microsteps(microsteps);

  SoftSerial1.end();
  
  Serial.println("-----Initialized Set Up-----");
  digitalWrite(EN_PIN_1,HIGH); 
  digitalWrite(EN_PIN_2,HIGH);
} 
 
void loop() { 
   
  char xBuffer[4]; 
  char yBuffer[4]; 
 
  memset(xBuffer, '\0', sizeof(xBuffer)); 
  memset(yBuffer, '\0', sizeof(yBuffer)); 
    
  if (Serial.available()>0) { 
    // Read the X and Y coordinates as strings 
    Serial.readBytesUntil(',', xBuffer, 4); 
    Serial.readBytesUntil('\n', yBuffer, 4); 
    Serial.println(xBuffer); 
    Serial.println(yBuffer);
    
    SoftSerial.begin(115200); 
    Serial.println(driver.microsteps());
    SoftSerial.end();
    
    SoftSerial1.begin(115200); 
    Serial.println(driver1.microsteps());
    SoftSerial1.end();
    if (strcmp(xBuffer, "0") == 0 && strcmp(yBuffer, "0") == 0) { 
      target_X=0.0; 
      target_Y=0.0; 
      calculateMovement(target_X,target_Y,current_X,current_Y); 
      move_to_coordinate(move_X , move_Y, 1, 10); 
      current_X = target_X; 
      current_Y = target_Y; 
    } 
    else{ 
      int inputX = atoi(xBuffer);
      int inputY = atoi(yBuffer);  
      int idx = 0;

      // Assuming 4 cm error on x and y axis
      Coordinate neighbors[81];
      gen(inputX,inputY, neighbors);
      voltage = 4;

      while ((voltage > 2.5 || voltage < 0.8) & idx < 81){
        int sensorValue = analogRead(analogPin); // read the analog input
        voltage = sensorValue * (5.0 / 1023.0); // convert the analog value to voltage
        // Serial.println("Voltage is: ..");
        // Serial.println(voltage);
        convertToSteps(inputX, inputY); 
        calculateMovement(target_X,target_Y,current_X,current_Y);
        if (idx == 0){
          move_to_coordinate(move_X , move_Y, 1, 10); 
          Serial.println("Current X: " + String(current_X) + ", Current Y: " + String(current_Y) + ", Target X: " + String(target_X) + ", Target Y: " + String(target_Y) + ", Move by X: " + String(move_X) + ", Move by Y: " + String(move_Y) + ", ----------------");

        } else {
          move_to_coordinate(move_X , move_Y, 0, 50); 
        }

        if (0 <= neighbors[idx].x && neighbors[idx].x <= 17 && 0 <= neighbors[idx].y && neighbors[idx].y <= 17) {
            inputX = neighbors[idx].x;
            inputY = neighbors[idx].y;
        }

        current_X = target_X;
        current_Y = target_Y;
        idx++;
      }
      
} 
    
    } 
} 
void convertToSteps(int xStr, int yStr) { 
  // Convert the strings to floats 
  float inputX = xStr; 
  float inputY = yStr; 
  if ( inputX == 0 ){ 
    target_X = 0; 
  } 
  else{ 
    target_X = inputX*10 / stepSize; 
  } 
  if ( inputY == 0 ){ 
    target_Y = 0; 
  } 
  else{ 
    target_Y = inputY*10 / stepSize; 
  } 
  // Calculate step sizes based on your defined step size 
} 
void calculateMovement(float targetX, float targetY, float currentX, float currentY) { 
  // Calculate the difference between target and current positions 
  move_X =round(targetX - currentX); 
  move_Y =round(targetY - currentY); 
} 
 
void move_to_coordinate(int deltaX, int deltaY, int flag, int delay){ 
  // positive_negative_X(deltaX); 
  // positive_negative_Y(deltaY); 
  pos_neg_xy(deltaX, deltaY, flag, delay); 
} 

void pos_neg_xy(int deltaX, int deltaY, int flag, int delay) { 
  int norm = (abs(deltaX) + abs(deltaY))/2; 
  float nrm = (abs(deltaX) + abs(deltaY))/2; 
  int Current_X = 0;  //Current X position 
  int unit_X;
  int unit_Y;
  if (deltaX == 0){
    unit_X = 0;
    nrm = (abs(deltaY));
    norm = abs(deltaY);
  } else {
    unit_X = deltaX/abs(deltaX);
  }


  int Current_Y = 0;  //Current Y position 
  if (deltaY == 0){
    unit_Y = 0;
    nrm = abs(deltaX);
    norm = abs(deltaX);
  } else {
    unit_Y = deltaY/abs(deltaY);
  }

// Serial.println("This is the norm"); 
  // Serial.println(norm); 
  int cnt = 0; 
  while (cnt < norm){ 
      if (unit_X == 1){ 
        //Serial.println("passed to stepper bro"); 
        moveStepper(0,STEP_PIN_1,DIR_PIN_1, nrm, deltaX, flag, delay); 
        moveStepper(0,STEP_PIN_2,DIR_PIN_2, nrm, deltaX, flag, delay); 
        // 
        Current_X = Current_X + unit_X; 
      }  else if (unit_X == -1) { 
        //Serial.println("passed to stepper bro"); 
        moveStepper(1,STEP_PIN_1,DIR_PIN_1, nrm, deltaX, flag, delay); 
        moveStepper(1,STEP_PIN_2,DIR_PIN_2, nrm, deltaX, flag, delay); 
          // 
        Current_X = Current_X + unit_X;   
      } 

      if (unit_Y > 0 ){ 
        //Serial.println("passed to stepper bro"); 
        moveStepper(1,STEP_PIN_1,DIR_PIN_1, nrm, deltaY, flag, delay); 
        moveStepper(0,STEP_PIN_2,DIR_PIN_2, nrm, deltaY, flag, delay); 
        // 
        Current_Y = Current_Y + unit_Y;    
      } else if (unit_Y < 0 ){ 
        //Serial.println("passed to stepper bro"); 
        moveStepper(0,STEP_PIN_1,DIR_PIN_1, nrm, deltaY, flag, delay); 
        moveStepper(1,STEP_PIN_2,DIR_PIN_2, nrm, deltaY, flag, delay); 
        // 
        Current_Y = Current_Y + unit_Y;    
      } 
      cnt++; 
  } 
}
void moveStepper(int direction, int step_pin, int dir_pin, float norm, int d, int flag, int delay) { 
  digitalWrite(EN_PIN_1,LOW); 
  digitalWrite(EN_PIN_2,LOW); 
  //driver.toff(3); 
  //driver1.toff(3); 
  // direction: 0 for clockwise, 1 for counterclockwise 
  digitalWrite(dir_pin, direction == 0 ? LOW : HIGH); 
  float temp = 0.95*abs(d)/norm; 
  int new_step = temp*steps; 
  for (long int i = 0; i < new_step; i++) { 
    if (flag == 0) {
      int sensorValue = analogRead(analogPin);
      voltage = sensorValue * (5.0 / 1023.0);
      if (voltage < 2.5 & voltage > 0.8) {
        // stop all movement
        break;
      } 
    }
    digitalWrite(step_pin, HIGH); 
    delayMicroseconds(delay);  // Adjust delay for motor speed 
    digitalWrite(step_pin, LOW); 
    delayMicroseconds(delay);  // Adjust delay for motor speed 
  } 
  //driver.toff(0); 
  //driver1.toff(0); 
  digitalWrite(EN_PIN_1,HIGH); 
  digitalWrite(EN_PIN_2,HIGH); 
}