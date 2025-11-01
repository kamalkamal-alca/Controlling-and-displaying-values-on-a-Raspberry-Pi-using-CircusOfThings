Circus of Things Raspberry Pi control and display values
Control GPIO LEDs (4 LEDs) on my Raspberry Pi with Circus of Things
Using Python, control a GPIO 32 pin (fan) with PWM and display the temperature from a sensor on this platform.

- Install the following libraries: requests, json, and W1ThermSensor
- Create a circusofthings.com account
- In https://circusofthings.com/workshop, create a new signal and name it control_led1, control_led2, control_led3, control_led4, etc.
- Here, we use a 74HC595 shift register to control the 4 LEDs separately for each command sent from each button.

- Key: 28440 for led1 (example)

- Key: 28441 for pwm (example)

- Key: 28442 for temp_c (example)

- Key: 28443 for temp_f (example)

- Go to https://circusofthings.com/dashboard,

- Click on View: Add a view to monitor the value of an existing signal.

- Choose a View to create the pwm interface, etc.

- Choose control_led1, etc., with a button (depending on the number of outputs you want)

- Run the code, control led1, led2, etc., via the dashboard buttons.
