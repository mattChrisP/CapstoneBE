// Define pin connections & motor's steps per revolution
const int EN_PIN_1 = 9;
const int EN_PIN_2 = 10;
const int DIR_PIN_1 = 3;
const int STEP_PIN_1= 4;
const int DIR_PIN_2 = 5;
const int STEP_PIN_2= 6;
const int stepsPerRevolution = 200;
const float stepSize = (3.0 / 50.0) * PI; // mm
float current_X = 0.0;
float current_Y = 0.0;
float target_X = 0.0;
float target_Y = 0.0;
int move_X = 0;
int move_Y = 0;
int steps = 16;

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

void setup(){ 
  Serial.begin(9600);
 // Declare pins as Outputs
  pinMode(A0, INPUT);

  pinMode(EN_PIN_1,OUTPUT);
  pinMode(EN_PIN_2,OUTPUT);
  pinMode(STEP_PIN_1, OUTPUT);
  pinMode(DIR_PIN_1, OUTPUT);
  pinMode(STEP_PIN_2, OUTPUT);
  pinMode(DIR_PIN_2, OUTPUT);
  digitalWrite(EN_PIN_1,HIGH);
  digitalWrite(EN_PIN_2,HIGH);
  Serial.println("-----Initialized Set Up-----");
}
void loop(){
 // Set motor direction clockwise
  char xBuffer[4];
  char yBuffer[4];

  float inputx;
  float inputy;

  memset(xBuffer, '\0', sizeof(xBuffer));
  memset(yBuffer, '\0', sizeof(yBuffer));

  if (Serial.available()>0) {
    // Read the X and Y coordinates as strings
    Serial.readBytesUntil(',', xBuffer, 4);
    Serial.readBytesUntil('\n', yBuffer, 4);
    // No need to do search motion
    if (strcmp(xBuffer, "0") == 0 && strcmp(yBuffer, "0") == 0) {
      target_X=0.0;
      target_Y=0.0;
      calculateMovement(target_X,target_Y,current_X,current_Y);
      move_to_coordinate(move_X , move_Y, 10, 1);
      current_X = target_X;
      current_Y = target_Y;
    }
    else{
      int inputX = atoi(xBuffer);
      int inputY = atoi(yBuffer);   
      int idx = 0;

      // Assuming 1 cm error on x and y axis
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
          move_to_coordinate(move_X , move_Y, 5, 1);
        } else {
          move_to_coordinate(move_X , move_Y, 5, 0);
        }
        
        
        if (0 <= neighbors[idx].x && neighbors[idx].x <= 17 && 0 <= neighbors[idx].y && neighbors[idx].y <= 17) {
            inputX = neighbors[idx].x;
            inputY = neighbors[idx].y;
        }
        //Serial.println("Current X: " + String(current_X) + ", Current Y: " + String(current_Y) + ", Target X: " + String(target_X) + ", Target Y: " + String(target_Y) + ", Move by X: " + String(move_X) + ", Move by Y: " + String(move_Y) + ", ----------------");

        current_X = target_X;
        current_Y = target_Y;
        idx++;
      }

    }
    
    }
}
  
void convertToSteps(int xStr, int yStr) {
  // Convert the strings to floats
  int inputX = xStr;
  int inputY = yStr;
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

void move_to_coordinate(int deltaX, int deltaY, int delay, int flag){
  // positive_negative_X(deltaX);
  // positive_negative_Y(deltaY);

  pos_neg_xy(deltaX, deltaY, delay, flag);
}
void pos_neg_xy(int deltaX, int deltaY, int delay, int flag) {
  int norm = (abs(deltaX) + abs(deltaY))/2;
  float nrm = (abs(deltaX) + abs(deltaY))/2;
  int Current_X = 0;  //Current X position
  int unit_X = deltaX/abs(deltaX);

  int Current_Y = 0;  //Current Y position
  int unit_Y = deltaY/abs(deltaY);

  // Serial.println("This is the norm");
  // Serial.println(norm);
  int cnt = 0;
  while (cnt < norm){
      if (unit_X == 1){
        //Serial.println("passed to stepper bro");
        moveStepper(0,STEP_PIN_1,DIR_PIN_1, nrm, deltaX, delay, flag);
        moveStepper(0,STEP_PIN_2,DIR_PIN_2, nrm, deltaX, delay, flag);
        //
        Current_X = Current_X + unit_X;
      }  else if (unit_X == -1) {
        //Serial.println("passed to stepper bro");
        moveStepper(1,STEP_PIN_1,DIR_PIN_1, nrm, deltaX, delay, flag);
        moveStepper(1,STEP_PIN_2,DIR_PIN_2, nrm, deltaX, delay, flag);
          //
        Current_X = Current_X + unit_X;  
      }
    
      if (unit_Y > 0 ){
        //Serial.println("passed to stepper bro");
        moveStepper(0,STEP_PIN_1,DIR_PIN_1, nrm, deltaY, delay, flag);
        moveStepper(1,STEP_PIN_2,DIR_PIN_2, nrm, deltaY, delay, flag);
        //
        Current_Y = Current_Y + unit_Y;   
      } else if (unit_Y < 0 ){
        //Serial.println("passed to stepper bro");
        moveStepper(1,STEP_PIN_1,DIR_PIN_1, nrm, deltaY, delay, flag);
        moveStepper(0,STEP_PIN_2,DIR_PIN_2, nrm, deltaY, delay, flag);
        //
        Current_Y = Current_Y + unit_Y;   
      }
      cnt++;
  }
}
  
  
void moveStepper(int direction, int step_pin, int dir_pin, float norm, int d, int delay, int flag) {
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