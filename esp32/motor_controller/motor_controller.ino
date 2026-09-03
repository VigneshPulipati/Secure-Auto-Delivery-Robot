#include <ros.h>
#include <geometry_msgs/Twist.h>

// ============================================================
// Autonomous Indoor Delivery Robot
// ESP32 Motor Controller
//
// ROS topic:
//     /cmd_vel  -> geometry_msgs/Twist
//
// Serial:
//     57600 baud
//
// Motor drivers:
//     L298N #1 -> Left side motors
//     L298N #2 -> Right side motors
// ============================================================


// ===================== L298N #1 =====================
// Left side
#define IN1 26
#define IN2 27
#define IN3 32
#define IN4 33
#define ENA 25
#define ENB 14


// ===================== L298N #2 =====================
// Right side
#define IN5 18
#define IN6 19
#define IN7 22
#define IN8 23
#define ENA2 21
#define ENB2 5


// ===================== ROS =====================

ros::NodeHandle nh;


// Motor PWM speed
// Range: 0 - 255
int motorSpeed = 185;


// ============================================================
// STOP
// ============================================================

void stopMotors()
{
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);

  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);

  digitalWrite(IN5, LOW);
  digitalWrite(IN6, LOW);

  digitalWrite(IN7, LOW);
  digitalWrite(IN8, LOW);

  analogWrite(ENA, 0);
  analogWrite(ENB, 0);

  analogWrite(ENA2, 0);
  analogWrite(ENB2, 0);
}


// ============================================================
// FORWARD
// ============================================================

void forward()
{
  // Left side forward
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);

  digitalWrite(IN5, HIGH);
  digitalWrite(IN6, LOW);

  // Right side forward
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);

  digitalWrite(IN7, HIGH);
  digitalWrite(IN8, LOW);

  analogWrite(ENA, motorSpeed);
  analogWrite(ENB, motorSpeed);

  analogWrite(ENA2, motorSpeed);
  analogWrite(ENB2, motorSpeed);
}


// ============================================================
// BACKWARD
// ============================================================

void backward()
{
  // Left side backward
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);

  digitalWrite(IN5, LOW);
  digitalWrite(IN6, HIGH);

  // Right side backward
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);

  digitalWrite(IN7, LOW);
  digitalWrite(IN8, HIGH);

  analogWrite(ENA, motorSpeed);
  analogWrite(ENB, motorSpeed);

  analogWrite(ENA2, motorSpeed);
  analogWrite(ENB2, motorSpeed);
}


// ============================================================
// TURN LEFT
// Left side backward
// Right side forward
// ============================================================

void turnLeft()
{
  // Left side backward
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);

  digitalWrite(IN5, LOW);
  digitalWrite(IN6, HIGH);

  // Right side forward
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);

  digitalWrite(IN7, HIGH);
  digitalWrite(IN8, LOW);

  analogWrite(ENA, motorSpeed);
  analogWrite(ENB, motorSpeed);

  analogWrite(ENA2, motorSpeed);
  analogWrite(ENB2, motorSpeed);
}


// ============================================================
// TURN RIGHT
// Left side forward
// Right side backward
// ============================================================

void turnRight()
{
  // Left side forward
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);

  digitalWrite(IN5, HIGH);
  digitalWrite(IN6, LOW);

  // Right side backward
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);

  digitalWrite(IN7, LOW);
  digitalWrite(IN8, HIGH);

  analogWrite(ENA, motorSpeed);
  analogWrite(ENB, motorSpeed);

  analogWrite(ENA2, motorSpeed);
  analogWrite(ENB2, motorSpeed);
}


// ============================================================
// ROS /cmd_vel CALLBACK
// ============================================================

void cmdVelCallback(const geometry_msgs::Twist& msg)
{
  float linear = msg.linear.x;
  float angular = msg.angular.z;


  // Forward
  if (linear > 0.1)
  {
    forward();
  }

  // Backward
  else if (linear < -0.1)
  {
    backward();
  }

  // Turn left
  else if (angular > 0.1)
  {
    turnLeft();
  }

  // Turn right
  else if (angular < -0.1)
  {
    turnRight();
  }

  // Stop
  else
  {
    stopMotors();
  }
}


// ROS subscriber
ros::Subscriber<geometry_msgs::Twist> sub(
  "cmd_vel",
  cmdVelCallback
);


// ============================================================
// SETUP
// ============================================================

void setup()
{
  // ROS Serial communication
  Serial.begin(57600);


  // Configure motor pins
  int pins[] = {
    IN1, IN2,
    IN3, IN4,
    IN5, IN6,
    IN7, IN8,
    ENA, ENB,
    ENA2, ENB2
  };

  for (int i = 0; i < 12; i++)
  {
    pinMode(pins[i], OUTPUT);
  }


  // Safety: motors OFF during startup
  stopMotors();


  // Initialize ROS
  nh.initNode();
  nh.subscribe(sub);
}


// ============================================================
// LOOP
// ============================================================

void loop()
{
  nh.spinOnce();

  delay(10);
}
