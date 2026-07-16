// Enhanced Dashboard with featured assets

let portfolioChart = null;

async function loadDashboard() {
    try {
        const token = localStorage.getItem('authToken');
        if (!token) {
            loadFeaturedAssets();
            return;
        }
        
        const portfolio = await api.getPortfolio();
        updateStats(portfolio);
        updateStockTable(portfolio);
        drawPortfolioChart(portfolio);
    } catch (error) {
        console.error('Error loading dashboard:', error);
        loadFeaturedAssets();
    }
}

async function loadFeaturedAssets() {
    try {
        const response = await api.getFeaturedAssets();
        displayFeaturedAssets(response.featured);
    } catch (error) {
        console.error('Error loading featured assets:', error);
        // Show default featured assets
        const defaultAssets = [
            { symbol: 'BTC', name: 'Bitcoin', type: 'crypto', price: 45230.50, change: '+5.2%', icon: '₿' },
            { symbol: 'GLD', name: 'Gold ETF', type: 'commodity', price: 195.45, change: '+1.8%', icon: '🏆' },
            { symbol: 'SLV', name: 'Silver ETF', type: 'commodity', price: 28.75, change: '+2.3%', icon: '💎' },
            { symbol: 'BTSD', name: 'Bitshares', type: 'crypto', price: 0.08234, change: '+0.8%', icon: '🔗' },
            { symbol: 'AAPL', name: 'Apple', type: 'stock', price: 150.25, change: '+3.1%', icon: '📱' },
            { symbol: 'TSLA', name: 'Tesla', type: 'stock', price: 242.30, change: '-1.5%', icon: '🚗' }
        ];
        displayFeaturedAssets(defaultAssets);
    }
}

function displayFeaturedAssets(assets) {
    const container = document.getElementById('featuredAssets');
    if (!container) return;
    
    container.innerHTML = '';
    
    assets.forEach(asset => {
        const changeClass = asset.change.startsWith('+') ? 'positive' : 'negative';
        const card = document.createElement('div');
        card.className = 'featured-card';
        card.style.cssText = `
            background: white;
            padding: 1rem;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            cursor: pointer;
            transition: transform 0.2s;
        `;
        card.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div>
                    <h4 style="color: #667eea; margin: 0 0 0.5rem 0;">${asset.icon} ${asset.name}</h4>
                    <p style="color: #999; margin: 0; font-size: 0.9rem;">${asset.symbol} • ${asset.type}</p>
                </div>
                <div style="text-align: right;">
                    <p style="font-size: 1.2rem; font-weight: bold; margin: 0;">$${asset.price.toFixed(2)}</p>
                    <p style="margin: 0; class="${changeClass}" class="${changeClass}">${asset.change}</p>
                </div>
            </div>
        `;
        card.onclick = () => addAssetToPortfolio(asset.symbol);
        container.appendChild(card);
    });
}

function addAssetToPortfolio(symbol) {
    showAddStockForm(symbol);
}

function updateStats(portfolio) {
    const totalValue = portfolio.stocks.reduce((sum, stock) => {
        return sum + (stock.currentPrice * stock.shares);
    }, 0);
    
    const investedValue = portfolio.stocks.reduce((sum, stock) => {
        return sum + (stock.purchasePrice * stock.shares);
    }, 0);
    
    const totalGain = totalValue - investedValue;
    const gainPercent = investedValue > 0 ? (totalGain / investedValue * 100).toFixed(2) : 0;
    
    document.getElementById('totalValue').textContent = `$${totalValue.toFixed(2)}`;
    document.getElementById('totalChange').textContent = `${gainPercent > 0 ? '+' : ''}${gainPercent}%`;
    document.getElementById('totalChange').className = gainPercent >= 0 ? 'stat-change positive' : 'stat-change negative';
    
    document.getElementById('holdingsCount').textContent = portfolio.stocks.length;
    
    const verificationStatus = portfolio.verified ? '✅ Verified' : '⏳ Pending';
    document.getElementById('verificationStatus').textContent = verificationStatus;
}

function updateStockTable(portfolio) {
    const tbody = document.getElementById('stockTableBody');
    tbody.innerHTML = '';
    
    portfolio.stocks.forEach(stock => {
        const value = stock.currentPrice * stock.shares;
        const gainLoss = value - (stock.purchasePrice * stock.shares);
        const gainPercent = stock.purchasePrice > 0 ? (gainLoss / (stock.purchasePrice * stock.shares) * 100).toFixed(2) : 0;
        
        const row = document.createElement('tr');
        row.innerHTML = `
            <td><strong>${stock.symbol}</strong></td>
            <td>${stock.shares}</td>
            <td>$${stock.currentPrice.toFixed(2)}</td>
            <td>$${value.toFixed(2)}</td>
            <td class="${gainLoss >= 0 ? 'positive' : 'negative'}">$${gainLoss.toFixed(2)}</td>
            <td class="${gainPercent >= 0 ? 'positive' : 'negative'}">${gainPercent > 0 ? '+' : ''}${gainPercent}%</td>
            <td>
                <button class="btn-secondary" onclick="editStock('${stock.symbol}')">Edit</button>
                <button class="btn-secondary" onclick="removeStockFromPortfolio('${stock.symbol}')">Remove</button>
            </td>
        `;
        tbody.appendChild(row);
        
        stockUpdater.addSymbol(stock.symbol);
    });
}

function drawPortfolioChart(portfolio) {
    const ctx = document.getElementById('portfolioChart').getContext('2d');
    
    const labels = portfolio.stocks.map(s => s.symbol);
    const values = portfolio.stocks.map(s => s.currentPrice * s.shares);
    const colors = [
        '#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe',
        '#43e97b', '#fa709a', '#fee140', '#30cfd0'
    ];
    
    if (portfolioChart) {
        portfolioChart.destroy();
    }
    
    portfolioChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: colors.slice(0, labels.length),
                borderColor: '#fff',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `$${context.parsed.toFixed(2)}`;
                        }
                    }
                }
            }
        }
    });
}

function showAddStockForm(preselectedSymbol = null) {
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.style.display = 'flex';
    modal.innerHTML = `
        <div class="modal-content">
            <span class="close" onclick="this.parentElement.parentElement.remove()">&times;</span>
            <h2>Add Asset to Portfolio</h2>
            <p style="color: #999; font-size: 0.9rem;">Stocks • Cryptocurrencies • Commodities</p>
            <input type="text" id="stockSymbol" placeholder="Symbol (e.g., AAPL, BTC, GLD)" class="input-field" value="${preselectedSymbol || ''}">
            <input type="number" id="stockShares" placeholder="Quantity" class="input-field" step="0.00001">
            <input type="number" id="stockPrice" placeholder="Purchase Price per Unit" class="input-field" step="0.01">
            <button class="btn-primary" onclick="addStockHandler()">Add to Portfolio</button>
        </div>
    `;
    document.body.appendChild(modal);
}

async function addStockHandler() {
    const symbol = document.getElementById('stockSymbol').value.toUpperCase();
    const shares = parseFloat(document.getElementById('stockShares').value);
    const price = parseFloat(document.getElementById('stockPrice').value);
    
    if (!symbol || !shares || !price) {
        alert('Please fill all fields');
        return;
    }
    
    try {
        await api.addStock({ symbol, shares, purchasePrice: price });
        loadDashboard();
        document.querySelector('.modal').remove();
        alert('Asset added successfully!');
    } catch (error) {
        alert('Error adding asset: ' + error.message);
    }
}

async function removeStockFromPortfolio(symbol) {
    if (confirm(`Remove ${symbol} from portfolio?`)) {
        try {
            await api.removeStock(symbol);
            loadDashboard();
        } catch (error) {
            alert('Error removing asset: ' + error.message);
        }
    }
}

function editStock(symbol) {
    alert(`Edit ${symbol} - implement edit functionality`);
}

stockUpdater.subscribe((data) => {
    const cells = document.querySelectorAll(`[data-symbol="${data.symbol}"]`);
    cells.forEach(cell => {
        cell.textContent = `$${data.currentPrice.toFixed(2)}`;
    });
});

window.addEventListener('DOMContentLoaded', () => {
    loadDashboard();
    setInterval(loadDashboard, 30000);
});