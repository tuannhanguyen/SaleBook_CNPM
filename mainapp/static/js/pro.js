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
        stats.innerText = `${data.total_quantity} `;
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

function del_item(itemId){
    if( confirm("Xóa khỏi giỏ hàng ?") == true){
        fetch(`/api/cart/${itemId}`, {
            'method': 'DELETE',
            'headers': {
            'Content-Type': 'application/json'
        }
        }).then(res=> res.json()).then(data =>{
           if(data.code == 200)
           {
                var x = document.getElementById(`item${data.item_id}`)
                x.style.display = 'none';
           }else{
                alert('Xoa that bai')
           }
        }).catch(err =>alert('Xoa that bai'))
    }
}

function updateItem(obj, itemId){
    fetch(`/api/cart/${itemId}`, {
        'method': 'post',
        'body': JSON.stringify({
            'quantity': obj.value
        }),
        'headers': {
            'Content-Type': 'application/json'
        }
        }).then(res => res.json()).then(data =>{
            if(data.code != 200)
                alert("Cap nhat that bai")
            else{
                document.getElementById('total_quantity').innerText = data.total_quantity;
                document.getElementById('total_amount').innerText = data.total_amount;
            }
                console.log("Thanh cong")
        }).catch(err => console.log("Cap nhat that bai"));
}