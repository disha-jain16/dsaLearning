"""
Simple Boids flocking simulation.
Run with: python boids.py
Requires: matplotlib

This script creates a window showing moving boids that follow
alignment, cohesion, and separation rules. Press close to stop.
"""
import random
import math
import sys

try:
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation
except Exception as e:
    print("matplotlib is required to run this simulation.\nInstall with: pip install matplotlib")
    raise

WIDTH, HEIGHT = 10.0, 10.0

class Boid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(0.5, 1.5)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed

    def update(self, boids, dt=0.1):
        # Parameters
        neighbor_dist = 1.5
        max_speed = 2.0
        max_force = 0.05

        # Rules accumulators
        align_x = align_y = 0.0
        coh_x = coh_y = 0.0
        sep_x = sep_y = 0.0
        total = 0

        for other in boids:
            if other is self:
                continue
            dx = other.x - self.x
            dy = other.y - self.y
            # Toroidal distance
            if dx > WIDTH / 2: dx -= WIDTH
            if dx < -WIDTH / 2: dx += WIDTH
            if dy > HEIGHT / 2: dy -= HEIGHT
            if dy < -HEIGHT / 2: dy += HEIGHT

            dist = math.hypot(dx, dy)
            if dist < neighbor_dist and dist > 0:
                # Alignment
                align_x += other.vx
                align_y += other.vy
                # Cohesion
                coh_x += other.x
                coh_y += other.y
                # Separation (inverse)
                sep_x += -dx / (dist * dist)
                sep_y += -dy / (dist * dist)
                total += 1

        ax = ay = 0.0
        if total > 0:
            # Average alignment
            align_x /= total
            align_y /= total
            mag = math.hypot(align_x, align_y) or 1.0
            align_x = (align_x / mag) * max_speed - self.vx
            align_y = (align_y / mag) * max_speed - self.vy

            # Cohesion: steer toward average position
            coh_x = (coh_x / total) - self.x
            coh_y = (coh_y / total) - self.y
            # Wrap cohesion vector for torus
            if coh_x > WIDTH / 2: coh_x -= WIDTH
            if coh_x < -WIDTH / 2: coh_x += WIDTH
            if coh_y > HEIGHT / 2: coh_y -= HEIGHT
            if coh_y < -HEIGHT / 2: coh_y += HEIGHT
            magc = math.hypot(coh_x, coh_y) or 1.0
            coh_x = (coh_x / magc) * max_speed - self.vx
            coh_y = (coh_y / magc) * max_speed - self.vy

            # Separation already computed
            mag_s = math.hypot(sep_x, sep_y) or 1.0
            sep_x = (sep_x / mag_s) * max_speed - self.vx
            sep_y = (sep_y / mag_s) * max_speed - self.vy

            # Weigh rules
            ax = align_x * 1.0 + coh_x * 0.6 + sep_x * 1.5
            ay = align_y * 1.0 + coh_y * 0.6 + sep_y * 1.5

            # Limit force
            fmag = math.hypot(ax, ay)
            if fmag > max_force:
                ax = (ax / fmag) * max_force
                ay = (ay / fmag) * max_force

        # Integrate
        self.vx += ax
        self.vy += ay
        # Limit speed
        speed = math.hypot(self.vx, self.vy)
        if speed > max_speed:
            self.vx = (self.vx / speed) * max_speed
            self.vy = (self.vy / speed) * max_speed

        self.x += self.vx * dt
        self.y += self.vy * dt

        # Wrap around (toroidal space)
        if self.x < 0: self.x += WIDTH
        if self.x >= WIDTH: self.x -= WIDTH
        if self.y < 0: self.y += HEIGHT
        if self.y >= HEIGHT: self.y -= HEIGHT


def make_boids(n=50):
    return [Boid(random.uniform(0, WIDTH), random.uniform(0, HEIGHT)) for _ in range(n)]


def animate_boids():
    boids = make_boids(80)

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0, WIDTH)
    ax.set_ylim(0, HEIGHT)
    ax.set_xticks([])
    ax.set_yticks([])
    scat = ax.scatter([b.x for b in boids], [b.y for b in boids], s=30)

    def update(frame):
        for b in boids:
            b.update(boids, dt=0.1)
        scat.set_offsets([(b.x, b.y) for b in boids])
        return scat,

    ani = FuncAnimation(fig, update, interval=30)
    plt.show()


if __name__ == '__main__':
    try:
        animate_boids()
    except KeyboardInterrupt:
        print('Exiting')
