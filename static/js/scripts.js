// ===========  Setting place bid input value and restrict value
// less than last bid price ==========
let previous_bid = document.getElementById('bid_price');
previous_bid.value = parseInt(previous_bid.value) + 1;
previous_bid.setAttribute('min', previous_bid.value);


// ======  Edit bid price ========
function edit_bid_price(bid_h_id) {
    document.getElementById("btn_edit_price_" + bid_h_id).style.display = "none";
    document.getElementById("btn_edit_price_save_" + bid_h_id).style.display = "inline-block";
    document.getElementById("btn_edit_price_cancel_" + bid_h_id).style.display = "inline-block";

    let bid_price = document.getElementById("bid_price_" + bid_h_id);
    let bid_price_input = document.getElementById("bid_price_input_" + bid_h_id);

    let bid_price_data = bid_price.innerText;

    bid_price.style.display = 'none';
    bid_price_input.style.display = "inline-block";
}

function save_edit_bid_price(bid_h_id) {
    let bid_price_input = document.getElementById("bid_price_input_" + bid_h_id);
    let new_price = bid_price_input.value;
    // alert(new_price);
    bid_price_input.value = new_price;
    document.getElementById('update_bid_form_' + bid_h_id).submit();
    bid_price_input.style.display = 'none';

    document.getElementById("bid_price_" + bid_h_id).style.display = 'inline-block';
    document.getElementById("btn_edit_price_" + bid_h_id).style.display = "inline-block";

    document.getElementById("btn_edit_price_save_" + bid_h_id).style.display = "none";
    document.getElementById("btn_edit_price_cancel_" + bid_h_id).style.display = "none";
}

function cancel_edit_bid_price(bid_h_id) {
    let bid_price_input = document.getElementById("bid_price_input_" + bid_h_id);
    bid_price_input.style.display = 'none';

    document.getElementById("bid_price_" + bid_h_id).style.display = 'inline-block';
    document.getElementById("btn_edit_price_" + bid_h_id).style.display = "inline-block";

    document.getElementById("btn_edit_price_save_" + bid_h_id).style.display = "none";
    document.getElementById("btn_edit_price_cancel_" + bid_h_id).style.display = "none";
}

