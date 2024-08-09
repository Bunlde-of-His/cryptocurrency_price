document.getElementById('price-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    const exchange = document.getElementById('exchange').value;
    const pair = document.getElementById('pair').value;

    let url = '/prices';
    const params = [];
    if (exchange) params.push(`exchange=${exchange}`);
    if (pair) params.push(`pair=${pair}`);
    if (params.length) url += `?${params.join('&')}`;

    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();

        const pricesDiv = document.getElementById('prices');
        pricesDiv.innerHTML = '';
        for (const [key, value] of Object.entries(data)) {
            const priceElement = document.createElement('p');
            priceElement.innerHTML = `<strong>${key}</strong> - Bid: ${value.bid.toFixed(2)}, Ask: ${value.ask.toFixed(2)}, Average: ${value.average.toFixed(2)}`;
            pricesDiv.appendChild(priceElement);
        }
    } catch (error) {
        console.error('Fetch error: ', error);
        const pricesDiv = document.getElementById('prices');
        pricesDiv.innerHTML = `<p style="color: red;">Error fetching data: ${error.message}</p>`;
    }
});



