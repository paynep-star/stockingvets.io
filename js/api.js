// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';
const STOCK_API_KEY = 'YOUR_STOCK_API_KEY';

// API Utility Functions
const api = {
    async request(endpoint, options = {}) {
        const token = localStorage.getItem('authToken');
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };
        
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        
        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`, {
                ...options,
                headers
            });
            
            if (!response.ok) {
                throw new Error(`API Error: ${response.statusText}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },
    
    async login(email, password) {
        return this.request('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });
    },
    
    async googleLogin(idToken) {
        return this.request('/auth/google', {
            method: 'POST',
            body: JSON.stringify({ idToken })
        });
    },
    
    async signup(userData) {
        return this.request('/auth/signup', {
            method: 'POST',
            body: JSON.stringify(userData)
        });
    },
    
    async submitVerification(verificationData) {
        const formData = new FormData();
        formData.append('fullName', verificationData.fullName);
        formData.append('dateOfBirth', verificationData.dateOfBirth);
        formData.append('twitter', verificationData.twitter);
        formData.append('discord', verificationData.discord);
        formData.append('linkedin', verificationData.linkedin);
        
        if (verificationData.idFile) {
            formData.append('idDocument', verificationData.idFile);
        }
        
        return this.request('/verification/submit', {
            method: 'POST',
            body: formData,
            headers: {}
        });
    },
    
    async getPortfolio() {
        return this.request('/portfolio');
    },
    
    async addStock(stockData) {
        return this.request('/portfolio/add', {
            method: 'POST',
            body: JSON.stringify(stockData)
        });
    },
    
    async removeStock(symbol) {
        return this.request(`/portfolio/${symbol}`, {
            method: 'DELETE'
        });
    },
    
    async getStockPrice(symbol) {
        return this.request(`/stocks/${symbol}/price`);
    },
    
    async getStockHistory(symbol, days = 30) {
        return this.request(`/stocks/${symbol}/history?days=${days}`);
    },
    
    async getForumThreads(page = 1) {
        return this.request(`/forum/threads?page=${page}`);
    },
    
    async createThread(threadData) {
        return this.request('/forum/threads', {
            method: 'POST',
            body: JSON.stringify(threadData)
        });
    },
    
    async getThreadResponses(threadId) {
        return this.request(`/forum/threads/${threadId}/responses`);
    },
    
    async postResponse(threadId, content) {
        return this.request(`/forum/threads/${threadId}/responses`, {
            method: 'POST',
            body: JSON.stringify({ content })
        });
    },
    
    async getTopContributors() {
        return this.request('/forum/contributors/top');
    },
    
    async getProfile() {
        return this.request('/user/profile');
    },
    
    async updateProfile(profileData) {
        return this.request('/user/profile', {
            method: 'PUT',
            body: JSON.stringify(profileData)
        });
    },
    
    async getVerificationStatus() {
        return this.request('/user/verification-status');
    }
};

class StockPriceUpdater {
    constructor() {
        this.symbols = [];
        this.listeners = [];
    }
    
    addSymbol(symbol) {
        if (!this.symbols.includes(symbol)) {
            this.symbols.push(symbol);
            this.startUpdates();
        }
    }
    
    removeSymbol(symbol) {
        this.symbols = this.symbols.filter(s => s !== symbol);
    }
    
    subscribe(callback) {
        this.listeners.push(callback);
    }
    
    startUpdates() {
        setInterval(async () => {
            for (let symbol of this.symbols) {
                try {
                    const data = await api.getStockPrice(symbol);
                    this.notify(data);
                } catch (error) {
                    console.error(`Error updating ${symbol}:`, error);
                }
            }
        }, 5000);
    }
    
    notify(data) {
        this.listeners.forEach(listener => listener(data));
    }
}

const stockUpdater = new StockPriceUpdater();