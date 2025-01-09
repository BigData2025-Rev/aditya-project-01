document.addEventListener('DOMContentLoaded', function () {
    const activeTab = document.querySelector('.nav-link.active');
    if (activeTab) {
      console.log('Default active tab:', activeTab.id);
      if (activeTab.id=='orders-tab') {
        fetchOrders();
      }
      if (activeTab.id == 'products-tab' || activeTab.id == 'admin-products-tab') {
        fetchAllProducts();
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
        console.log('Tab clicked:', tab.id);
      });
    });


    const statusTab = document.getElementById('')
  
    const tablookup = {
        'orders-tab': fetchOrders,
        'products-tab': fetchProducts,
        'admin-products-tab': fetchAllProducts,
        'admin-users-tab': fetchAllUsers,
        'admin-orders-tab': fetchAllOrders
    }

    const observer = new MutationObserver(function(mutationsList) {
    for (let mutation of mutationsList) {
    if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
        const tab = mutation.target;
        if (tab.classList.contains('active')) {
        tablookup[tab.id]()
        console.log('Active tab changed to:', tab.textContent);
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
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;

    if (!username || !password) {
        showError('Please enter both username and password.');
        return;
    }

    const response = await fetch('http://localhost:8888/login', {
        method: 'POST',
        headers: {
            'Origin': "http://localhost:3000",
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
    console.log(JSON.stringify({ username, password, email, country}))
    try {
        const response = await fetch('http://localhost:8888/register', {
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
    const response = await fetch('http://localhost:8888/getallusers', {
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
    console.log(users)
    const tableBody = document.querySelector('#admin-users tbody');
    tableBody.innerHTML = '';
    users.forEach(user => {
        const row = document.createElement('tr');
        console.log(user);
        row.innerHTML = `
            <td>${user['username']}</td>
            <td>${user['email']}</td>
            <td>${user['role']}</td>`;
        tableBody.appendChild(row);
    });

}

async function fetchProducts() {
    const products_tab = document.getElementById('products-tab')
    const authToken = localStorage.getItem('authToken');
    const response = await fetch('http://localhost:8888/products',{
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
    const tableBody = document.querySelector('#products tbody');
    tableBody.innerHTML = '';

    products.forEach(product => {
        const row = document.createElement('tr');
        console.log(product);
        row.innerHTML = `<td>${product['name']}</td>
                         <td>${product['stock']}</td>
                        <td>$${product['price']}</td>
                        <td><button onclick="addtoCart(${product['product_id']})">Purchase Product</button></td>`;
        tableBody.appendChild(row);
    });
}

async function fetchAllOrders() {
    const users_tab = document.getElementById('admin-orders-tab');
    const authToken = localStorage.getItem('authToken');
    const response = await fetch('http://localhost:8888/getallorders',{
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
            order = JSON.parse(order);
            statusId = order['order_id'];
            statusString = order['order_status'];
            optionString = ``;
            for (let key in status) {
                if (key == statusString) {
                    optionString += `<option value="${key}" selected>` + `${status[key]}` + `</option>`
                } else {
                    optionString += `<option value="${key}" >` + `${status[key]}` + `</option>`
                }        
            }

            row.innerHTML = `<td>${order['order_id']}</td>
                            <td>${order['order_status']}</td>
                            <td><select id="${statusId}">` + optionString +
                            `</select>
                            </td>`;
            tableBody.appendChild(row);
        });
    } else {
        const p = document.createElement('p')
        p.innerHTML = "You don't have any orders yet!"
    }
}

async function editOrderStatus(event) {
    console.log(event.target.id)
    const id = event.target.id
    order_status = event.target.value;
    console.log(order_status)
    const authToken = localStorage.getItem('authToken');
    const response = await fetch(`http://localhost:8888/order/update/${id}`,{
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
    const response = await fetch('http://localhost:8888/products',{
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
        console.log(product);
        row.innerHTML = `<td>${product['product_id']}</td>
                         <td>${product['name']}</td>
                         <td>${product['stock']}</td>
                        <td>$${product['price']}</td>
                        <td><button onclick="editProduct(${product['product_id']})">Edit Product</button></td>`;
        tableBody.appendChild(row);
    });
}

async function editProduct(order_id) {
    const authToken = localStorage.getItem('authToken');
    const response = await fetch('http://localhost:8888/order', {
                                method: 'POST',
                                headers: {
                                    "Authorization": "Bearer " + authToken
                                },
                                body: JSON.stringify({
                                    "product_id" : product_id,
                                    "quantity": quantity
                                    })
                            });
    const data = await response.json();
    console.log(data)
    if(!response.ok) {
        alert("Could not add order to cart!");
    }
}

async function addtoCart(product_id, quantity=1) {
    const authToken = localStorage.getItem('authToken');
    const response = await fetch('http://localhost:8888/order', {
                                method: 'POST',
                                headers: {
                                    "Authorization": "Bearer " + authToken
                                },
                                body: JSON.stringify({
                                    "product_id" : product_id,
                                    "quantity": quantity
                                    })
                            });
    if(!response.ok) {
        alert("Could not add order to cart!");
    }

}

async function fetchOrders() {
    const order_tab = document.getElementById('orders-tab')
    const authToken = localStorage.getItem('authToken');
    const response = await fetch('http://localhost:8888/orders',{
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
    if (orders) {
        const tableBody = document.querySelector('#orders tbody');
        tableBody.innerHTML = '';
        orders.forEach(order => {
            const row = document.createElement('tr');
            value = JSON.parse(order);
            row.innerHTML = `
                <td>${value['order_id']}</td>
                <td>${value['order_status']}</td>`;
            tableBody.appendChild(row);
        });
    } else {
        const p = document.createElement('p')
        p.innerHTML = "You don't have any orders yet!"
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

