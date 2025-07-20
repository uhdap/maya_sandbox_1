import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(page_title="Consciousness Agent Sandbox", page_icon="🧠", layout="wide")

# Title and description
st.title("🧠 Consciousness Agent Sandbox")
st.write("Wu-wei inspired token economy simulation with Yin-Yang-Qi triad agents")

# Initialize session state
if 'agents' not in st.session_state:
    st.session_state.agents = {
        'yang': {'bias': +1, 'maya': 1000, 'history': []},
        'yin': {'bias': -1, 'maya': 1000, 'history': []},
        'swing': {'bias': 0, 'maya': 1000, 'history': []}
    }
    st.session_state.time_step = 0

# Sidebar
st.sidebar.header("⚙️ Controls")
st.sidebar.write("Configure your conscious agents:")

# User inputs
initial_maya = st.sidebar.slider("Initial MAYA tokens:", 100, 2000, 1000)
stimulus = st.sidebar.slider("Environment stimulus:", -1.0, 1.0, 0.0)
action_cost = st.sidebar.slider("Base action cost:", 1, 10, 5)
time_steps = st.sidebar.number_input("Simulation steps:", 1, 100, 10)

# Reset button
if st.sidebar.button("🔄 Reset Agents"):
    for agent in st.session_state.agents.values():
        agent['maya'] = initial_maya
        agent['history'] = []
    st.session_state.time_step = 0

# Main content
col1, col2 = st.columns(2)

with col1:
    st.subheader("💰 Agent Token Economy")
    
    # Display agent states
    for name, agent in st.session_state.agents.items():
        delta = agent['maya'] - initial_maya
        st.metric(
            f"{name.capitalize()} (bias: {agent['bias']:+d})", 
            f"{agent['maya']} MAYA",
            f"{delta:+d}"
        )
    
    # Token history chart
    if any(agent['history'] for agent in st.session_state.agents.values()):
        st.subheader("📊 Token History")
        
        # Prepare data for plotting
        fig, ax = plt.subplots()
        for name, agent in st.session_state.agents.items():
            if agent['history']:
                ax.plot(agent['history'], label=name.capitalize(), marker='o')
        
        ax.set_xlabel('Time Step')
        ax.set_ylabel('MAYA Tokens')
        ax.set_title('Agent Token Evolution')
        ax.legend()
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)

with col2:
    st.subheader("🎯 Agent Behavior")
    
    # Calculate agent responses
    responses = {}
    costs = {}
    
    for name, agent in st.session_state.agents.items():
        # Cost based on distance from bias
        cost = abs(stimulus - agent['bias']) * action_cost + 1
        costs[name] = cost
        
        # Can agent afford action?
        if agent['maya'] >= cost:
            responses[name] = agent['bias'] * np.tanh(stimulus)
        else:
            responses[name] = 0  # No action if broke
    
    # Display responses
    st.write(f"**Current Stimulus:** {stimulus:.2f}")
    
    response_df = pd.DataFrame({
        'Agent': list(st.session_state.agents.keys()),
        'Bias': [a['bias'] for a in st.session_state.agents.values()],
        'Response': list(responses.values()),
        'Cost': list(costs.values()),
        'Can Act': [a['maya'] >= costs[name] for name, a in st.session_state.agents.items()]
    })
    
    st.dataframe(response_df)
    
    # Consensus calculation
    if any(responses.values()):
        weights = [a['maya'] for a in st.session_state.agents.values()]
        total_weight = sum(weights)
        if total_weight > 0:
            consensus = sum(w * r for w, r in zip(weights, responses.values())) / total_weight
            st.metric("Triad Consensus", f"{consensus:.3f}")

# Simulation section
st.divider()
st.subheader("🧪 Run Simulation")

if st.button("▶️ Run Simulation"):
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for step in range(time_steps):
        # Generate random stimulus
        step_stimulus = np.random.normal(0, 0.5)
        
        # Update each agent
        for name, agent in st.session_state.agents.items():
            cost = abs(step_stimulus - agent['bias']) * action_cost + 1
            
            if agent['maya'] >= cost:
                agent['maya'] -= cost
                agent['history'].append(agent['maya'])
        
        st.session_state.time_step += 1
        
        # Update progress
        progress_bar.progress((step + 1) / time_steps)
        status_text.text(f"Step {step + 1}/{time_steps}")
    
    status_text.text("Simulation complete!")
    st.rerun()

# Expandable section
with st.expander("ℹ️ About this sandbox"):
    st.write("""
    This consciousness sandbox implements:
    - **Triad Architecture**: Yang (+1), Yin (-1), and Swing (0) agents
    - **Token Economy**: MAYA tokens as internal currency for actions
    - **Wu-Wei Principle**: Agents act based on natural bias, not reward-seeking
    - **Path Dependence**: Token history tracks agent evolution
    - **Consensus Emergence**: Weighted consensus from agent responses
    
    Agents spend tokens based on the distance between stimulus and their bias.
    The more "unnatural" the action, the more tokens it costs.
    """)

# Display ledger preview
if st.checkbox("Show Agent Ledgers"):
    st.write("**Agent States:**")
    st.json(st.session_state.agents)