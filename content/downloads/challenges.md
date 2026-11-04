# Try a small challenge


Speed: change SPEED by 20. Hint: 0–255 is a duty range, not RPM. Record whether wheels start.

Sensor reporter: print digitalRead(34) once every 200 ms using millis. Hint: keep reporting bounded so serial traffic does not delay decisions.

Line search: change lastTurn's initial sign. Predict the first search direction before running.

Obstacle preference: choose right when both sides clear. Update code and decision table together.

Failsafe: send one F and time how soon it stops. Do not remove the timeout to make driving easier.

Before each change, save a copy. Restore the original if the result is unclear. Ask the teacher to review code before applying power.


Check your understanding

How will you tell whether your change improved behavior?
