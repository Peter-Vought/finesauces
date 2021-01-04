// Get the current year for the copyright
$('#year').text(new Date().getFullYear());

// init tooltips
$('[data-toggle="tooltip"]').tooltip();

// define UI vars
const minusBtn = document.querySelector('#minus');
const plusBtn = document.querySelector('#plus');
const form_control = document.querySelector('.form-control')

loadEventListeners();
function loadEventListeners() {
    try{
        minusBtn.addEventListener('click', decreaseAmount);
        plusBtn.addEventListener('click', increaseAmount);
    }
    catch(e){}

    try{
        document.addEventListener('DOMContentLoaded',  setTotalCost);
    }
    catch(e){}
}

function decreaseAmount(){
    let currentAmount = document.getElementById('id_quantity').value;
    
    if(currentAmount - 1 > 0){
        currentAmount--;
        document.getElementById('id_quantity').value = String(currentAmount);
    }
}

function increaseAmount(){
    let currentAmount = Number(document.getElementById('id_quantity').value);
    currentAmount++;
    document.getElementById('id_quantity').value = String(currentAmount);
}

function setTotalCost() {
    
    let totalCost = Number(document.getElementById("cart_price").innerText);
    totalCost += getSumOfElements('transport');
    totalCost = totalCost.toFixed(2);
    // set total price
    document.getElementById("order-total").innerHTML = `$${totalCost}`
}

function getSumOfElements(elementName){
    let sum = 0;
    radios = document.getElementsByName(elementName);
    for(let i = 0; i < radios.length; i++){
        if(radios[i].checked){
            if(radios[i].getAttribute('amount') !== 'free'){
                sum += Number(radios[i].getAttribute('amount'));
            }
        }
    }

    return sum;
}