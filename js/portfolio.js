async function loadPortfolio() {
    try {
        const token = localStorage.getItem('authToken');
        if (!token) return;
        
        const portfolio = await api.getPortfolio();
        displayPortfolio(portfolio);
    } catch (error) {
        console.error('Error loading portfolio:', error);
    }
}

function displayPortfolio(portfolio) {
    const content = document.getElementById('portfolioContent');
    
    if (portfolio.stocks.length === 0) {
        content.innerHTML = '<p>Your portfolio is empty. Add your first stock!</p>';
        return;
    }
    
    let html = '<div class="section">';
    
    portfolio.stocks.forEach(stock => {
        const value = stock.currentPrice * stock.shares;
        const gain = value - (stock.purchasePrice * stock.shares);
        const gainPercent = stock.purchasePrice > 0 ? (gain / (stock.purchasePrice * stock.shares) * 100).toFixed(2) : 0;
        const gainClass = gain >= 0 ? 'positive' : 'negative';
        
        html += `
            <div class="stock-card" style="background: white; padding: 1.5rem; margin: 1rem 0; border-radius: 8px; border-left: 4px solid #667eea; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                <h3>${stock.symbol}</h3>
                <p><strong>Shares:</strong> ${stock.shares}</p>
                <p><strong>Current Price:</strong> $${stock.currentPrice.toFixed(2)}</p>
                <p><strong>Total Value:</strong> $${value.toFixed(2)}</p>
                <p><strong>Cost Basis:</strong> $${(stock.purchasePrice * stock.shares).toFixed(2)}</p>
                <p class="${gainClass}"><strong>Gain/Loss:</strong> $${gain.toFixed(2)} (${gainPercent > 0 ? '+' : ''}${gainPercent}%)</p>
                <div style="margin-top: 1rem;">
                    <button class="btn-primary" onclick="updateStockPosition('${stock.symbol}')">Update</button>
                    <button class="btn-secondary" onclick="sellStock('${stock.symbol}')">Sell</button>
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    content.innerHTML = html;
}

function updateStockPosition(symbol) {
    alert(`Update position for ${symbol} - implement update form`);
}

function sellStock(symbol) {
    alert(`Sell ${symbol} - implement sell form`);
}

window.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('portfolio')) {
        loadPortfolio();
    }
});