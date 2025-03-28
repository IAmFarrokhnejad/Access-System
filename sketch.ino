#include <Keypad.h>

// Keypad configuration
const byte ROWS = 4;
const byte COLS = 4;
char hexKeys[ROWS][COLS] = {
  {'1','2','3','A'},
  {'4','5','6','B'},
  {'7','8','9','C'},
  {'*','0','#','D'}
};
byte rowPins[ROWS] = {9, 8, 7, 6};
byte colPins[COLS] = {5, 4, 3, 2};
Keypad keypad = Keypad(makeKeymap(hexKeys), rowPins, colPins, ROWS, COLS);

// LED configuration
const int GREEN_LED = 10;
const int RED_LED = 11;
const int BLUE_LED = 12;

void setup() {
  Serial.begin(9600);
  pinMode(GREEN_LED, OUTPUT);
  pinMode(RED_LED, OUTPUT);
  pinMode(BLUE_LED, OUTPUT);
  set_leds(LOW, LOW, LOW);
}

void loop() {
  handle_keypad();
  handle_serial();
}

void handle_keypad() {
  char key = keypad.getKey();
  if (key) {
    Serial.println(key);
  }
}

void handle_serial() {
  if (Serial.available() > 0) {
    char cmd = Serial.read();
    switch(cmd) {
      case 'G':  // Access granted
        set_leds(HIGH, LOW, LOW);
        delay(5000);
        set_leds(LOW, LOW, LOW);
        break;
      case 'R':  // Access denied
        set_leds(LOW, HIGH, LOW);
        delay(5000);
        set_leds(LOW, LOW, LOW);
        break;
      case 'P':  // Face scan in progress
        set_leds(LOW, LOW, HIGH);
        break;
      case 'L':  // System locked
        set_leds(LOW, HIGH, LOW);
        delay(60000);
        set_leds(LOW, LOW, LOW);
        break;
      case 'X':  // Reset
        set_leds(LOW, LOW, LOW);
        break;
    }
  }
}

void set_leds(int green, int red, int blue) {
  digitalWrite(GREEN_LED, green);
  digitalWrite(RED_LED, red);
  digitalWrite(BLUE_LED, blue);
}