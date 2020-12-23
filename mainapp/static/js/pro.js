function addToCart(id, name, price){
    fetch('/api/cart', {
    'method': 'post',
    'body': JSON.stringify({
        'id': id,
        'name': name,
        'price': price
    }),
    'headers': {
        'Content-Type': 'application/json'
    }
    }).then(res => res.json()).then(data =>{
        console.info(data);
        var stats = document.getElementById("cart-stats")
        stats.innerText = `${data.total_quantity} - ${data.total_amount} vnd`;
    })
}