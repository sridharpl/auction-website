const BACKEND_URL = "https://auction-website.streamlit.app/";

const bidForm = document.getElementById('bid-form');
const bidHistory = document.getElementById('bid-history');
const totalQuantityEl = document.getElementById('total-quantity');
const highestBidEl = document.getElementById('highest-bid');
const timeRemainingEl = document.getElementById('time-remaining');

async function fetchAuctionStats() {
    try {
        const response = await fetch(`${BACKEND_URL}/api/auction-stats`);
        const stats = await response.json();

        if (stats.success) {
            totalQuantityEl.textContent = stats.remaining_quantity;
            highestBidEl.textContent = stats.highest_bid;
            timeRemainingEl.textContent = stats.time_remaining;
        } else {
            alert(stats.message || "Failed to fetch auction stats.");
        }
    } catch (error) {
        console.error('Error fetching auction stats:', error);
    }
}

bidForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const quantity = document.getElementById('quantity').value;
    const price = document.getElementById('price').value;

    try {
        const response = await fetch(`${BACKEND_URL}/api/submit-bid`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ quantity, price }),
        });

        const result = await response.json();

        if (result.success) {
            const bidEntry = document.createElement('li');
            bidEntry.textContent = `Quantity: ${quantity}, Price: ${price}`;
            bidHistory.appendChild(bidEntry);
        } else {
            alert(result.message);
        }
    } catch (error) {
        console.error('Error submitting bid:', error);
    }
});

setInterval(fetchAuctionStats, 5000); // Refresh stats every 5 seconds