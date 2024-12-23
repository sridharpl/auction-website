const BACKEND_URL = "https://your-backend-url.com"; // Replace with your backend URL

// Create auction functionality
document.getElementById('create-auction-form').addEventListener('submit', async (event) => {
    event.preventDefault();

    const formData = new FormData(event.target);
    const auctionData = Object.fromEntries(formData.entries());

    try {
        const response = await fetch(`${BACKEND_URL}/api/admin/create-auction`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(auctionData),
        });

        const result = await response.json();

        if (result.success) {
            alert("Auction created successfully.");
            event.target.reset();
        } else {
            alert(result.message || "Failed to create auction.");
        }
    } catch (error) {
        console.error('Error creating auction:', error);
    }
});

// Fetch results functionality
async function fetchResults() {
    try {
        const response = await fetch(`${BACKEND_URL}/api/results`);
        const result = await response.json();

        if (result.success) {
            const resultsTable = document.getElementById('results-table').querySelector('tbody');
            resultsTable.innerHTML = '';

            result.results.forEach((res) => {
                const row = `
                    <tr>
                        <td>${res.phone_number}</td>
                        <td>${res.allocated_quantity}</td>
                        <td>${res.price}</td>
                    </tr>
                `;
                resultsTable.innerHTML += row;
            });
        } else {
            alert(result.message || "Failed to fetch auction results.");
        }
    } catch (error) {
        console.error('Error fetching results:', error);
    }
}

// Fetch results on page load
document.addEventListener('DOMContentLoaded', fetchResults);