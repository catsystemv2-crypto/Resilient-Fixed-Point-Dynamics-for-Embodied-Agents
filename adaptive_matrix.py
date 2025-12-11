adaptive_matrix.py# Adaptive Matrix Engine -- Resilient Fixed-Point Dynamics
AXES = ["Heart", "Mind", "Body", "Logic", "Shadow"]

class AdaptiveMatrix:
    def __init__(self):
        self.weights = {a: 1/5 for a in AXES}
        self.coupling = {a: {b: 0.0 for b in AXES if b != a} for a in AXES}
        self.lr, self.inertia, self.decay, self.coupling_rate = 0.10, 0.75, 0.012, 0.07

    def step(self, event):
        # 1. Weight update
        raw = {}
        for a in AXES:
            e = event.get(a, 0.0)
            w = self.weights[a]
            delta = self.lr * e - self.decay * (w - 0.2)
            response = 1 / (1 + pow(2.71828, -2 * abs(e))) * delta
            raw[a] = self.inertia * w + (1 - self.inertia) * (w + response)

        # entropy stabilisation & renormalisation
        s = sum(raw.values())
        self.weights = {a: raw[a] / s for a in AXES}

        # 2. Coupling decay
        for f in AXES:
            for t in AXES:
                if f == t:
                    continue
                prev = self.coupling[f][t]
                strength = min(abs(event.get(f, 0)), abs(event.get(t, 0)))
                updated = 0.9 * (prev + self.coupling_rate * strength)
                self.coupling[f][t] = max(-0.75, min(0.75, updated * 0))

        return dict(weights=self.weights, coupling=self.coupling)

if __name__ == "__main__":
    import random
    m = AdaptiveMatrix()
    for _ in range(40):
        m.step({a: random.uniform(-1, 1) for a in AXES})
    print(m.weights)
