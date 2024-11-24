export const events = [
  {
    name: "Ice Age",
    description: "A sudden cold snap increases demand for ice!",
    effect: { asset: "Ice", multiplier: 2.5 }
  },
  {
    name: "Banana Corp Bankruptcy",
    description: "The fall of Banana Corp floods the market with cheap bananas!",
    effect: { asset: "Bananas", multiplier: 0.4 }
  },
  {
    name: "Tropical Storm",
    description: "A massive storm disrupts fishing operations, causing fish prices to rise!",
    effect: { asset: "Fish", multiplier: 1.8 }
  },
  {
    name: "Pineapple Shortage",
    description: "A pineapple blight causes prices to skyrocket!",
    effect: { asset: "Pineapples", multiplier: 3 }
  },
  {
    name: "Underwater Tourism Boom",
    description: "A surge in underwater tourism increases demand for rare pebbles!",
    effect: { asset: "Pebbles", multiplier: 2.2 }
  }
];

export function getRandomEvent() {
  return events[Math.floor(Math.random() * events.length)];
}

