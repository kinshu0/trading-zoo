# Trading Zoo!

A Playful Market Simulation Game

## Overview

Trading Zoo is a whimsical trading simulation game that brings the world of finance to life through anthropomorphized animal teams. Set in a jungle-themed environment, the game features various animal species as sophisticated trading teams, each with their own specialties and trading strategies.

![image](https://github.com/user-attachments/assets/7a848a97-3c52-4520-bc62-c28f1d0a0e13)


## Core Concept

Players can observe and interact with a vibrant marketplace where animal teams trade exotic goods in real-time. The game combines educational aspects of market dynamics with playful, jungle-themed elements.
![image](https://github.com/user-attachments/assets/26be7083-b5fb-4074-b767-c5fefa96d7a7)


## Trading Teams

* **Penguins** 🐧 - Cool-headed traders specializing in ice futures
* **Monkeys** 🐒 - Agile merchants expert in fruit trading
* **Foxes** 🦊 - Cunning market analysts and strategic traders
* **Iguanas** 🦎 - Patient long-term investors

## Tradable Assets

* **Bananas** 🍌 - A staple commodity
* **Ice** 🧊 - Temperature-sensitive luxury good
* **Pineapples** 🍍 - Exotic fruit commodity
* **Fish** 🐟 - For the best sushi
* **Pebbles** 💎 - Beach treasure

![image](https://github.com/user-attachments/assets/b0dc73c5-0447-421f-abbe-d01f0caa4874)


## Game Features

* Real-time trading simulation
* Dynamic price fluctuations
* Random market events affecting prices
* Team performance tracking
* Visual data representation through graphs
* Detailed trade history
* Jungle-themed UI with playful animations

## Technical Architecture

### Multi-Agent Trading System

Trading Zoo implements a sophisticated multi-agent trading environment powered by AutoGen, where AI agents engage in market activities through a central trading engine. Each animal team is represented by an autonomous LLaMA-based agent capable of processing market information and making independent trading decisions.

### Core Components

* **Trading Engine**
  * Centralized matching engine for order execution
  * Real-time orderbook management
  * Price discovery mechanism
  * Transaction logging and settlement

* **Market Maker Agent**
  * Provides baseline market liquidity
  * Maintains bid-ask spreads
  * Helps prevent extreme price volatility
  * Facilitates efficient price discovery

* **Trading Agents (Animal Teams)**
  * Each agent receives:
    * Current portfolio status
    * Real-time orderbook data
    * Market event notifications
    * Historical price data
  * Autonomous decision-making based on:
    * Team-specific trading strategies
    * Market conditions analysis
    * Risk management parameters
    * Portfolio objectives

### System Integration

```
[Market Events] → [Trading Engine] ← [Market Maker]
       ↓              ↑    ↓
[Order Book] → [Trading Agents] ← [Portfolio Data]
```

### Implementation Details

* Built using AutoGen's multi-agent conversation framework
* Each agent operates as an independent entity with its own strategy and goals
* Real-time communication through event-driven architecture
* Asynchronous order processing and matching
* State management for portfolio and transaction history

### Data Flow

1. Market events are broadcast to all agents
2. Agents analyze their portfolio and market data
3. Trading decisions are converted to orders
4. Orders are submitted to the central trading engine
5. Market maker provides counterparty when needed
6. Matching engine executes valid trades
7. Portfolio and market data are updated
8. Trading agents receive execution feedback

This multi-agent system creates a dynamic, self-sustaining marketplace where AI-driven animal teams can engage in realistic trading activities while maintaining market stability through the market maker's presence.

## Educational Value

While maintaining a fun and accessible atmosphere, the game teaches fundamental concepts of:

* Supply and demand
* Market dynamics
* Price fluctuations
* Trading strategies
* Risk management
* Portfolio tracking

## Target Audience

Trading Zoo is designed for:

* Beginners interested in learning about trading
* Students learning economics
* Anyone interested in gamified financial education
* Casual gamers who enjoy management simulations

The game strikes a balance between educational value and entertainment, using the jungle theme and animal characters to make complex market concepts more approachable and engaging.


### Instructions to Run Trading Zoo

Backend:
```
cd backend
uv sync
uv run game.py
```

Frontend:
```
cd frontend
npm i
npm run start
```
