import numpy as np
import random

# -------------------------
# GLOBAL PARAMETERS
# -------------------------
GAMMA = 0.95  # discount factor

# -------------------------
# STATE SPACE
# -------------------------
class State:
    def __init__(self):
        # Physical variables
        self.positions = np.random.rand(5, 3)   # satellites in 3D
        self.debris_density = np.random.rand()  # K
        
        # Latent legal variables (unobservable)
        self.intent = np.random.choice(["peaceful", "hostile"])
        self.authorization = np.random.choice(["authorized", "deviant"])
        self.control_logic = np.random.choice(["human", "AI"])

# -------------------------
# ACTION SPACE
# -------------------------
class Action:
    def __init__(self):
        # Operational
        self.a_O = np.random.choice(["safe", "risky"])
        
        # Strategic (Chicken)
        self.a_S = np.random.choice(["persist", "evade"])
        
        # Regulation (Article VI)
        self.m = np.random.choice(["high", "low"])
        
        # Signal
        self.sigma = np.random.choice(["transparent", "ambiguous"])
        
        # Verification
        self.v = np.random.choice(["high", "low"])

# -------------------------
# OBSERVATION FUNCTION Ω
# -------------------------
def observation_function(state):
    obs = {}
    
    # Noisy observation of physical state
    obs["positions"] = state.positions + np.random.normal(0, 0.1, state.positions.shape)
    obs["debris_density"] = state.debris_density + np.random.normal(0, 0.05)
    
    # Latent variables NOT observable
    # (intent, authorization, control_logic hidden)
    
    return obs

# -------------------------
# TRANSITION FUNCTION T
# -------------------------
def transition(state, actions):
    new_state = State()
    
    # Debris evolves stochastically
    risk_factor = sum([1 if a.a_O == "risky" else 0 for a in actions])
    new_state.debris_density = min(1.0, state.debris_density + 0.1 * risk_factor + np.random.rand()*0.05)
    
    # Random collision probability
    collision_prob = 0.05 + 0.2 * risk_factor
    if random.random() < collision_prob:
        new_state.debris_density += 0.3  # collision increases debris
    
    return new_state

# -------------------------
# PAYOFF FUNCTION R_i
# -------------------------
def payoff(action, state, obs):
    # V_i: operational value
    V = 1.0 if action.a_S == "persist" else 0.5
    
    # C(K): congestion
    C = state.debris_density
    
    # E: escalation risk (based on ambiguity)
    E = 0.5 if action.sigma == "ambiguous" else 0.2
    
    # I: information tax
    I = 0.5 if action.m == "high" else 0.1
    
    return V - C - E - I

# -------------------------
# PLAYER
# -------------------------
class Player:
    def __init__(self, name):
        self.name = name
    
    def choose_action(self, obs):
        # Placeholder: random policy
        return Action()

# -------------------------
# MASTER GAME LOOP
# -------------------------
def run_simulation(num_players=3, steps=50):
    players = [Player(f"P{i}") for i in range(num_players)]
    state = State()
    
    for t in range(steps):
        observations = [observation_function(state) for _ in players]
        actions = [players[i].choose_action(observations[i]) for i in range(num_players)]
        
        # Compute payoffs
        rewards = [payoff(actions[i], state, observations[i]) for i in range(num_players)]
        
        print(f"Step {t}: Debris={state.debris_density:.2f}, Rewards={rewards}")
        
        # Transition
        state = transition(state, actions)

# Run
run_simulation()
