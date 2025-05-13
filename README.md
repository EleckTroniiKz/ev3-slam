# 🤖 ev3-slam

A university robotics project developed during our 6th semester. We used a LEGO EV3 robot running Python to implement real-time **SLAM** (Simultaneous Localization and Mapping) using a **Particle Filter** for localization and a **Quadtree** structure for map representation.

---

## 🚀 Overview

**ev3-slam** enables a LEGO Mindstorms EV3 robot to explore an unknown environment, localize itself using sensor data, and build a spatial map using a quadtree representation. The robot fuses data from its **gyroscope** (for rotation) and **infrared sensor** (for distance measurements), feeding into a **particle filter** to estimate its pose.

> 💡 Built as a hands-on robotics project during our university's embedded systems course.

---

## 🧠 Key Features

- 🧭 SLAM with **Particle Filter**
- 🌲 Environment mapping using a **Quadtree**
- 📡 Sensor fusion with **Gyroscope** + **Infrared Sensor**
- 📍 localization and map updating
- 🐍 Fully implemented in **Python**
- 🧱 Runs on LEGO EV3 hardware

---

## 📸 Demo

<!-- Replace with actual demo video/GIF if available -->
![Demo](https://media.giphy.com/media/26tPplGWjN0xLybiU/giphy.gif)

---

## 🛠️ Technologies Used

- **Python 3**
- **ev3dev** (Debian-based OS for LEGO EV3)
- **NumPy** (for matrix math and particles)
- **pygame** (for visualization)
- **Custom Quadtree** data structure for spatial map

---
