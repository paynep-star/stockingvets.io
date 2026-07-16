let portfolioChart = null;

async function loadDashboard() {
    try {
        const token = localStorage.getItem('authToken');
        if (!token) return;
        
        const portfolio = await api.getPortfolio();
        updateStats(portfolio);
        updateStockTable(portfolio);
        drawPortfolioChart(portfolio);
    } catch (error) {
        console.error('Error loading dashboard:', error);
    }
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

function showAddStockForm() {
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.style.display = 'flex';
    modal.innerHTML = `
        <div class="modal-content">
            <span class="close" onclick="this.parentElement.parentElement.remove()">&times;</span>
            <h2>Add Stock to Portfolio</h2>
            <input type="text" id="stockSymbol" placeholder="Stock Symbol (e.g., AAPL)" class="input-field">
            <input type="number" id="stockShares" placeholder="Number of Shares" class="input-field">
            <input type="number" id="stockPrice" placeholder="Purchase Price per Share" class="input-field">
            <button class="btn-primary" onclick="addStockHandler()">Add Stock</button>
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
        alert('Stock added successfully!');
    } catch (error) {
        alert('Error adding stock: ' + error.message);
    }
}

async function removeStockFromPortfolio(symbol) {
    if (confirm(`Remove ${symbol} from portfolio?`)) {
        try {
            await api.removeStock(symbol);
            loadDashboard();
        } catch (error) {
            alert('Error removing stock: ' + error.message);
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