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


function pay(){
    if (confirm("Thanh tóan giỏ hàng?") == true)
        fetch('/api/pay', {
        'method': 'post',
        'headers': {
            'Content-Type': 'application/json'
        }
        }).then(res => res.json()).then(data =>{
            alert(data.message);
            location.reload();
        }).catch(err => console.log(err))
}