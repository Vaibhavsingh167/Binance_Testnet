let ctx = document.getElementById('priceChart').getContext('2d');
let chart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [
            {
                label: 'BTC Price',
                data: [],
                borderColor: 'blue',
                fill: false
            },
            {
                label: 'Buy',
                data: [],
                borderColor: 'green',
                backgroundColor: 'green',
                type: 'scatter',
                pointRadius: 6,
                showLine: false
            },
            {
                label: 'Sell',
                data: [],
                borderColor: 'red',
                backgroundColor: 'red',
                type: 'scatter',
                pointRadius: 6,
                showLine: false
            }
        ]
    }
});

function fetchPrice() {
    fetch("/price")
        .then(res => res.json())
        .then(data => {
            if (data.price) {
                document.getElementById("price").innerText = data.price;
            }
        });
}

function fetchHistory() {
    fetch("/history")
        .then(res => res.json())
        .then(data => {
            chart.data.labels = data.prices.map(p => p[0]);
            chart.data.datasets[0].data = data.prices.map(p => p[1]);

            chart.data.datasets[1].data = data.trades
                .filter(t => t[2] === "BUY")
                .map(t => ({ x: t[0], y: t[1] }));

            chart.data.datasets[2].data = data.trades
                .filter(t => t[2] === "SELL")
                .map(t => ({ x: t[0], y: t[1] }));

            chart.update();
        });
}

function startBot() {
    fetch("/start", { method: "POST" })
        .then(res => res.json())
        .then(alert);
}

function stopBot() {
    fetch("/stop", { method: "POST" })
        .then(res => res.json())
        .then(alert);
}

setInterval(fetchPrice, 3000);
setInterval(fetchHistory, 3000);

fetchPrice();
fetchHistory();
