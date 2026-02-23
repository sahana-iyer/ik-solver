<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:000000,100:00FF41&height=180&section=header&text=IK-SOLVER&fontSize=60&fontColor=00FF41&animation=fadeIn&fontAlignY=35&desc=2DOF%20to%204DOF%20Inverse%20Kinematics%20Solver&descAlignY=55&descSize=16&descColor=00CC33" width="100%"/>

<img src="https://readme-typing-svg.demolab.com?font=Share+Tech+Mono&size=18&duration=3000&pause=1000&color=00FF41&center=true&vCenter=true&width=600&lines=Click+anywhere.+The+arm+follows.;Analytical+IK+%7C+Pygame+Visualisation;2DOF+%E2%86%92+3DOF+%E2%86%92+4DOF" alt="Typing SVG" />

</div>

---

### What is this?

A robotic arm simulator where you click anywhere on the screen and the arm moves to reach that point in real time. It calculates the joint angles needed using Inverse Kinematics.

Built progressively — starting from 2DOF and extending to 4DOF.

---

### Forward vs Inverse Kinematics — simply put

**Forward Kinematics (FK)**
You give it the joint angles → it tells you where the tip of the arm ends up.

**Inverse Kinematics (IK)**
You give it where you want the tip to go → it figures out what the joint angles need to be.

IK is the harder problem. This project solves it.

---

### How the math works (2DOF)

Imagine the two arm links and the straight line from base to target forming a **triangle**. You know all three side lengths — L1, L2, and the distance to the target.

- **Theta 2 (elbow angle)** — Law of cosines on that triangle gives you the elbow bend angle. Same formula from high school: `c² = a² + b² - 2ab·cos(C)`, rearranged to find the angle.

- **Theta 1 (shoulder angle)** — `atan2(y, x)` gives the direction from base to target. Subtract a correction for how much the elbow is bending. That gives you the shoulder angle.

That's the entire analytical solution. No black box, no neural network — just geometry.

---

### Progression

| Phase | DOF | Method | Status |
|---|---|---|---|
| Phase 1 | 2DOF | Analytical (Law of Cosines) | ✅ Done |
| Phase 2 | 3DOF | Jacobian Pseudoinverse | 🔲 Upcoming |
| Phase 3 | 4DOF | Jacobian Pseudoinverse + constraints | 🔲 Upcoming |

---

### Stack

<div align="center">

![Python](https://img.shields.io/badge/Python-000000?style=for-the-badge&logo=python&logoColor=00FF41)
![NumPy](https://img.shields.io/badge/NumPy-000000?style=for-the-badge&logo=numpy&logoColor=00FF41)
![Pygame](https://img.shields.io/badge/Pygame-000000?style=for-the-badge&logoColor=00FF41)

</div>

---

### Run it

```bash
git clone https://github.com/sahana-iyer/ik-solver.git
cd ik-solver
pip install pygame numpy
python ik_solver.py
```

Click anywhere in the window — the arm follows.

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:00FF41,100:000000&height=120&section=footer&animation=fadeIn" width="100%"/>

*Built by Sahana G Iyer — Part of the journey to Humanoid RL Agent*

</div>
