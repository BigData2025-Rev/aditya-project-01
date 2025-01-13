API_URL='http://localhost:8888'

document.addEventListener('DOMContentLoaded', function () {
    const activeTab = document.querySelector('.nav-link.active');
    if (activeTab) {
    //   console.log('Default active tab:', activeTab.id);
      if (activeTab.id=='orders-tab') {
        fetchOrders();
      }
      if ( activeTab.id == 'admin-products-tab') {
        fetchAllProducts();
      }
      if (activeTab.id == 'products-tab') {
        fetchProducts();
      }
      if (activeTab.id == 'admin-order-tab') {
        fetchAllOrders();
      }
      if (activeTab.id == 'admin-users-tab') {
        fetchAllUsers();
      }
    }

    const tabs = document.querySelectorAll('.nav-link');
    tabs.forEach(tab => {
      tab.addEventListener('click', function() {
        // console.log('Tab clicked:', tab.id);
      });
    });


    const statusTab = document.getElementById('')
  
    const tablookup = {
        'orders-tab': fetchOrders,
        'products-tab': fetchProducts,
        'admin-products-tab': fetchAllProducts,
        'admin-users-tab': fetchAllUsers,
        'admin-orders-tab': fetchAllOrders,
        'cart-tab': cart,
    }

    const observer = new MutationObserver(function(mutationsList) {
    for (let mutation of mutationsList) {
    if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
        const tab = mutation.target;
        if (tab.classList.contains('active')) {
        tablookup[tab.id]()
        // console.log('Active tab changed to:', tab.textContent);
        }
    }
    }
    });


    tabs.forEach(tab => {
      observer.observe(tab, { attributes: true });
    });

    const table = document.getElementById('admin-orders');
    table.addEventListener('change', function(event) {
        if (event.target.tagName.toLowerCase() === 'select') {
            editOrderStatus(event);
        }
    });
  });

function toggleForms() {
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    const errorMessage = document.getElementById('error-message');
    const errorMessageRegister = document.getElementById('error-message-register');
    
    loginForm.style.display = loginForm.style.display === 'none' ? 'block' : 'none';
    registerForm.style.display = registerForm.style.display === 'none' ? 'block' : 'none';

    errorMessage.style.display = 'none';
    errorMessageRegister.style.display = 'none';

}

async function login() {
    console.log("Called login!")
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;

    if (!username || !password) {
        showError('Please enter both username and password.');
        return;
    }

    const response = await fetch(`${API_URL}/login`, {
        method: 'POST',
        headers: {
            'Origin': `${API_URL}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    }).then(response => {
        if (!response.ok) {
            throw new Error("Response Status "+ response.status)
        }
        
        return response.json()
    }).then(data => {
        token = data.token;
        role = data.role;
        // console.log(data)
        if(token) {
            localStorage.setItem("authToken", token);
            if (role == 'user') {
                window.location.href = 'userdashboard.html';
            } 
            if (role == 'admin') {
                window.location.href = 'admindashboard.html';
            }
            
        }
    }).catch(error => {
        showError(error.message)
    });
}

async function register() {
    const username = document.getElementById('register-username').value;
    const password = document.getElementById('register-password').value;
    const email = document.getElementById('register-email').value;
    const country = document.getElementById('register-country').value;

    if (!username || !password) {
        showErrorRegister('Please enter both username and password.');
        return;
    }
    // console.log(JSON.stringify({ username, password, email, country}))
    try {
        const response = await fetch(`${API_URL}/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password, email, country})
        });

        if (response.ok) {
            alert("Registration successful! Please log in.");
            toggleForms();
        } else {
            const errorData = await response.json();
            showErrorRegister(errorData.message || "An error occurred during registration.");
        }
    } catch (error) {
        showErrorRegister("An error occurred. Please try again.");
    }
}

function showError(message) {
    if (message) {
        const errorMessageDiv = document.getElementById('error-message');
        errorMessageDiv.textContent = message;
        errorMessageDiv.style.display = 'block';
    }
}

function showErrorRegister(message) {
    if (message) {
        const errorMessageDiv = document.getElementById('error-message-register');
        errorMessageDiv.textContent = message;
        errorMessageDiv.style.display = 'block';
    }
}

function logout() {
    localStorage.removeItem('authToken');
    window.location.href = './main.html';
}

async function fetchAllUsers() {
    const users_tab = document.getElementById('admin-users-tab')
    const authToken = localStorage.getItem('authToken');
    const response = await fetch(`${API_URL}/getallusers`, {
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + authToken
        }
    })
    if (!response.ok) {
        localStorage.removeItem('authToken')
        window.location.href = "./main.html";
    }
    const data = await response.json();
    const users = data.users;
    // console.log(users)
    const tableBody = document.querySelector('#admin-users tbody');
    tableBody.innerHTML = '';
    users.forEach(user => {
        const row = document.createElement('tr');
        // console.log(user);
        row.innerHTML = `
            <td>${user['id']}</td>
            <td>${user['username']}</td>
            <td>${user['email']}</td>
            <td>${user['created_at']}</td>
            <td>${user['wallet_balance']}
            <td>${user['role']}</td>`;
        tableBody.appendChild(row);
    });
}

async function fetchProducts() {
    const products_tab = document.getElementById('products-tab')
    const authToken = localStorage.getItem('authToken');
    const response = await fetch(`${API_URL}/products`,{
                         method: 'GET',
                         headers: {
                            'Authorization': 'Bearer '+ authToken
                         }
                        });
    if (!response.ok) {
        // const tableBody = document.querySelector('#products tbody');
        // tableBody.innerHTML = '';
        localStorage.removeItem('authToken')
        window.location.href = "./main.html";
    }
    const data = await response.json();
    const products = JSON.parse(data.products);
    // console.log(products);
    const tableBody = document.querySelector('#products tbody');
    tableBody.innerHTML = '';

    products.forEach(product => {
        const row = document.createElement('tr');
        // console.log(product);
        row.innerHTML = `<td><img src="${product['image']}"/></td>
                        <td>${product['name']}</td>
                        <td>${product['stock']}</td>
                        <td>${product['price']}</td>
                        <td><button class="btn btn-primary" onclick="addToCart(${product['product_id']})">Add to Cart</button></td>`;
        tableBody.appendChild(row);
    });
}

async function fetchAllOrders() {
    const users_tab = document.getElementById('admin-orders-tab');
    const authToken = localStorage.getItem('authToken');
    const response = await fetch(`${API_URL}/getallorders`,{
                         method: 'GET',
                         headers: {
                            'Authorization': 'Bearer '+ authToken
                         }
                        });
    if (!response.ok) {
        localStorage.removeItem('authToken')
        window.location.href = "./main.html";
    }
    const data = await response.json();
    const orders = data.orders;
    const status = {'pending' : 'Pending',
                    'completed': 'Completed',
                    'delivered': 'Delivered',
                    'returned': 'Returned',
                    'canceled': 'Canceled',
                    'shipped': 'Shipped'};
    if (orders) {
        const tableBody = document.querySelector('#admin-orders tbody');
        tableBody.innerHTML = '';
        orders.forEach(order => {
            const row = document.createElement('tr');
            value = JSON.parse(order);
            // console.log(value)
            const statusId = value['order_id'];
            const statusString = value['order_status'];
            optionString = ``;
            for (let key in status) {
                if (key == statusString) {
                    optionString += `<option value="${key}" selected>` + `${status[key]}` + `</option>`
                } else {
                    optionString += `<option value="${key}" >` + `${status[key]}` + `</option>`
                }        
            }
            // // console.log(value)
            table = `<table><thead><th>Product Name</th><th>Quantity</th><th>Price</th>`;
            tableclose = `</thead></table>`;
            items = ``;
            // console.log(JSON.parse(value.items))
            if (value.items) {
                // console.log(value.items.length)
                value.items.forEach(item => {

                    jsonItem = JSON.parse(item)
                    // <li><img src="${item['product_image']}"/></li>
                    //<td><img src="${jsonItem['product_image']}"/></td>
                    items += `<tr><td>${jsonItem['product_name']}</td>
                              <td>${jsonItem['product_quantity']}</td>
                              <td>${jsonItem['product_price']}</td></tr>`;
                });
            }
            items += '</tr>'
            //
            row.innerHTML = `<td>${value['order_id']}</td>
                             <td>${table + items + tableclose}</td>
                             <td>${value['order_status']}</td>

                            <td><select id="${statusId}">` + optionString +`</select></td>`;
            tableBody.appendChild(row);
        });
    } else {
        const p = document.createElement('p')
        p.innerHTML = "You don't have any orders yet!"
    }
}

async function editOrderStatus(event) {
    // console.log(event.target.id)
    const id = event.target.id
    order_status = event.target.value;
    // console.log(order_status)
    const authToken = localStorage.getItem('authToken');
    const response = await fetch(`${API_URL}/order/update/${id}`,{
        method: 'PATCH',
        headers: {
           'Authorization': 'Bearer '+ authToken
        },
        body : JSON.stringify({ order_status })
       });
    const data = await response.json()
    if (response.ok) {
        fetchAllOrders();
    }
}

async function fetchAllProducts() {
    const products_tab = document.getElementById('admin-products-tab')
    const authToken = localStorage.getItem('authToken');
    const response = await fetch(`${API_URL}/products`,{
                         method: 'GET',
                         headers: {
                            'Authorization': 'Bearer '+ authToken
                         }
                        });
    if (!response.ok) {
        localStorage.removeItem('authToken')
        window.location.href = "./main.html";
    }
    const data = await response.json();
    const products = JSON.parse(data.products);
    const tableBody = document.querySelector('#admin-products tbody');
    tableBody.innerHTML = '';

    products.forEach(product => {
        const row = document.createElement('tr');
        // console.log(product);
        row.innerHTML = `<td>${product['product_id']}</td>
                        <td><img src="${product['image']}"/></td>
                         <td>${product['name']}</td>
                         <td>${product['stock']}</td>
                        <td>$${product['price']}</td>
                        <td><button class="btn btn-outline-danger" onclick="removeProduct(${product['product_id']})">Remove Product</button></td>`;
        tableBody.appendChild(row);
    });
}

async function removeProduct(product_id) {
    console.log(product_id);
    const authToken = localStorage.getItem('authToken');
    const response = await fetch(`${API_URL}/product/delete/${product_id}`, {
                                method: 'DELETE',
                                headers: {
                                    "Authorization": "Bearer " + authToken
                                }
                            });
    const data = await response.json();
    // console.log(data)
    alert(`${data.message}`)
    fetchAllProducts()
}

async function addToCart(product_id, quantity=1) {
    // userConfirmation = confirm("Are you sure you want to purchase the item? ")
    // if (!userConfirmation) {
    //     return
    // }
    const authToken = localStorage.getItem('authToken');
    const response = await fetch(`${API_URL}/order`, {
                                method: 'POST',
                                headers: {
                                    "Authorization": "Bearer " + authToken
                                },
                                body: JSON.stringify({
                                    "product_id" : product_id,
                                    "quantity": quantity
                                    })
                            });
    const data = await response.json()
    if(!response.ok) {
        alert(`Could not add order to cart! ${data.message}`);
    }
    fetchProducts()
}

async function fetchOrders() {
    const order_tab = document.getElementById('orders-tab')
    const authToken = localStorage.getItem('authToken');
    const response = await fetch(`${API_URL}/orders`,{
                         method: 'GET',
                         headers: {
                            'Authorization': 'Bearer '+ authToken
                         }
                        });
    if (!response.ok) {
        localStorage.removeItem('authToken')
        window.location.href = "./main.html";
    }
    const data = await response.json();
    const orders = data.orders;
    // console.log(data)
    if (orders) {
        const tableHead = document.querySelector('#orders thead');
        tableHead.innerHTML = '';
        tableHead.innerHTML = `<th>Order ID</th>
                  <th>Items</th>
                  <th>Status</th>`;
        const tableBody = document.querySelector('#orders tbody');
        tableBody.innerHTML = '';
        orders.forEach(order => {
            const row = document.createElement('tr');
            value = JSON.parse(order);
            // console.log(value)
            table = `<table><thead><th></th><th>Product Name</th><th>Quantity</th><th>Price</th>`;
                tableclose = `</thead></table>`;
            items = ``;
            value.items.forEach(item => {
                jsonItem = JSON.parse(item)
                // <li><img src="${item['product_image']}"/></li>
                items += `<tr><td><img src="${jsonItem['product_image']}"/></td>
                          <td>${jsonItem['product_name']}</td>
                          <td>${jsonItem['product_quantity']}</td>
                          <td>${jsonItem['product_price']}</tr>`;
            });
            row.innerHTML = `
                <td>${value['order_id']}</td>
                <td>${table + items + tableclose}</td>
                <td>${value['order_status']}</td>`;
            tableBody.appendChild(row);
        });
    } else {
        const tableHead = document.querySelector('#orders thead');
        tableHead.innerHTML = '';
        const tableBody = document.querySelector('#orders tbody');
        tableBody.innerHTML = '';
        const p = document.createElement('p')
        p.innerHTML = "You don't have any orders yet!"
        tableHead.appendChild(p)
    }
}

function dropdownOptions() {
    const menu = document.getElementById('dropdownMenuLink')
    if(menu) {
        menu.addEventListener('click', function () {
            var dropdownMenu = document.querySelector('.dropdown-menu');
            dropdownMenu.classList.toggle('show');
          });
    }
}

async function cart() {
    const authToken = localStorage.getItem('authToken');
    const response = await fetch(`${API_URL}/user/listcart`,{
                         method: 'GET',
                         headers: {
                            'Authorization': 'Bearer '+ authToken
                         }
                        });
    if (!response.ok) {
        localStorage.removeItem('authToken')
        window.location.href = "./main.html";
    }
    const data = await response.json();
    const orders = await data.orders;
    if(orders.length > 0) {
        document.getElementById("funds").style.display = "inline";
        document.getElementById("checkout").style.display = "inline";
        const tableHead = document.querySelector('#cart-content thead');
        tableHead.innerHTML = `<tr>
                                <th></th>
                                <th>Name</th>
                                <th>Status</th>
                                <th>Total</th>
                              </tr>`;
        const tableBody = document.querySelector('#cart-content tbody');
        tableBody.innerHTML = '';
        orders.forEach(order => {
            const row = document.createElement('tr');
            value = JSON.parse(order);
            // console.log(value)
            table = `<table><thead><th></th><th>Product Name</th><th>Quantity</th><th>Price</th>`;
            tableclose = `</thead></table>`;
            items = ``;
            value.items.forEach(item => {
                jsonItem = JSON.parse(item)
                // <li><img src="${item['product_image']}"/></li>
                items += `<tr><td><img src="${jsonItem['product_image']}"/></td>
                        <td>${jsonItem['product_name']}</td>
                        <td>${jsonItem['product_quantity']}</td>
                        <td>${jsonItem['product_price']}</td></tr>`;
            });
            row.innerHTML = `
                <td>${value['order_id']}</td>
                <td>${table + items + tableclose}</td>
                <td>${value['order_status']}</td>
                <td>${value['total_amount']}`;
            tableBody.appendChild(row);
        });
    }
    else {
        document.getElementById("funds").style.display = "none";
        document.getElementById("checkout").style.display = "none";
        const tableHead = document.querySelector('#cart-content thead');
        tableHead.innerHTML = '';
        const tableBody = document.querySelector('#cart-content tbody');
        tableBody.innerHTML = '';
        const p = document.createElement('p')
        p.innerHTML = "You don't have any items in the cart yet!"
        tableHead.appendChild(p)
    }
}


async function checkoutCart() {
    const authToken = localStorage.getItem('authToken');
    const response = await fetch(`${API_URL}/user/checkout`,{
                         method: 'POST',
                         headers: {
                            'Authorization': 'Bearer '+ authToken
                         }
                        });
    const data = await response.json();
    if (!response.ok) {
        alert(`Could not add order to cart! ${data.message}`);
    }
    cart()
}

async function addFunds() {
    deposit_amount = 500;
    userConfirmation = confirm(`Are you sure you like the deposit ${deposit_amount}? `)
    if (!userConfirmation) {
        return
    }
    const authToken = localStorage.getItem('authToken');

    const response = await fetch(`${API_URL}/user/addbalance`, {
        method: 'POST',
        headers: {
            'Authorization': 'Bearer ' + authToken
        },
        body : JSON.stringify({ deposit_amount })
    })
    const data = await response.json();
    if (!response.ok) {
        localStorage.removeItem('authToken')
        window.location.href = "./main.html";
    }
    alert(`${data.message}`)

}