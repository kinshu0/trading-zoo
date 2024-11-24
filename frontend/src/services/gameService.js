const API_BASE_URL = 'http://127.0.0.1:5000';

const defaultHeaders = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
};

export const gameService = {
  // Game state
  startGame: async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/start`, {
        method: 'GET',
        headers: defaultHeaders,
      });
      if (!response.ok) throw new Error('Network response was not ok');
      return response.text();
    } catch (error) {
      console.error('Start game error:', error);
      throw error;
    }
  },

  tick: async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/tick`, {
        method: 'GET',
        headers: defaultHeaders,
      });
      if (!response.ok) throw new Error('Network response was not ok');
      return response.text();
    } catch (error) {
      console.error('Tick error:', error);
      throw error;
    }
  },

  // Market data
  getSecurities: async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/securities`, {
        method: 'GET',
        headers: defaultHeaders,
      });
      if (!response.ok) throw new Error('Network response was not ok');
      return response.json();
    } catch (error) {
      console.error('Get securities error:', error);
      throw error;
    }
  },

  // Team/Client data
  registerClient: async (name) => {
    const response = await fetch(`${API_BASE_URL}/register/${name}`);
    return response.text();
  },

  getClients: async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/clients`, {
        method: 'GET',
        headers: defaultHeaders,
      });
      if (!response.ok) throw new Error('Network response was not ok');
      return response.json();
    } catch (error) {
      console.error('Get clients error:', error);
      throw error;
    }
  },

  getClientByName: async (name) => {
    const response = await fetch(`${API_BASE_URL}/client/${name}`);
    return response.text();
  },

  // Transactions
  getCompletedTransactions: async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/completed_transactions`, {
        method: 'GET',
        headers: defaultHeaders,
      });
      if (!response.ok) throw new Error('Network response was not ok');
      return response.json();
    } catch (error) {
      console.error('Get completed transactions error:', error);
      throw error;
    }
  },

  getPendingTransactions: async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/pending_transactions`, {
        method: 'GET',
        headers: defaultHeaders,
      });
      if (!response.ok) throw new Error('Network response was not ok');
      return response.json();
    } catch (error) {
      console.error('Get pending transactions error:', error);
      throw error;
    }
  },
}; 