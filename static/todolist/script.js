function add(name) {
    // Construct the URL with the provided name
    const url = '/add?item=' + encodeURIComponent(name);

    // Send a GET request to the endpoint
    fetch(url, {
        method: 'GET',
    })
    .then(response => {
        if (!response.ok) {
            // If server responds with a non-200 status, reject the promise
            return Promise.reject('Failed to add item');
        }
        update();
        return; // Assuming server responds with json
    })
    .then(data => {
        console.log('Item added successfully:', data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function update()
{
    var xhr = new XMLHttpRequest();

    xhr.open('GET', '/list', true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            var data = JSON.parse(xhr.responseText);

            var completedList = document.getElementById('completed-list');
            var notCompletedList = document.getElementById('not-completed-list');
            completedList.innerHTML = "";
            notCompletedList.innerHTML = "";

            for (let i = 0; i < data.length; i++) {
                console.log(data[i]._id);
                let label = document.createElement('label');
                label.className = 'checkbox-container';
                label.textContent = data[i].item;
                
                let span = document.createElement('span');
                span.className = 'checkmark';

                let checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                
                let temp=data[i]._id;
                checkbox.onclick = function() {toggle(temp);}
                
                let img=document.createElement('img');
                img.src='/static/todolist/trash.png';
                img.alt='trashcan'
                img.onclick = function(){remove(temp);}
                
                let listItem = document.createElement('li');
                
                label.appendChild(checkbox);
                listItem.appendChild(label);
                label.appendChild(img);
                label.appendChild(span);
                

                if (data[i].is_complete) {
                    checkbox.checked=true;
                    completedList.appendChild(listItem);
                } else {
                    notCompletedList.appendChild(listItem);
                }
            }
        }
    };
    xhr.send();
}

function process()
{
    let elem = document.getElementById('task_name');
    if(elem.value === "") return;
    add(elem.value);
    elem.value="";
}

function toggle(id) {
    console.log(id);
    // Construct the URL with the provided id
    const url = `/toggle/${id}`;

    // Send a GET request to the endpoint
    fetch(url, {
        method: 'GET',
    })
    .then(response => {
        if (!response.ok) {
            // If server responds with a non-200 status, reject the promise
            return Promise.reject('Failed to toggle item');
        }
        update();
        return; // Assuming server responds with json
    })
    .then(data => {
        console.log('Item toggled successfully:', data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function remove(id) {
    console.log(id);
    // Construct the URL with the provided id
    const url = `/remove/${id}`;

    // Send a GET request to the endpoint
    fetch(url, {
        method: 'GET',
    })
    .then(response => {
        if (!response.ok) {
            // If server responds with a non-200 status, reject the promise
            return Promise.reject('Failed to toggle item');
        }
        update();
        return; // Assuming server responds with json
    })
    .then(data => {
        console.log('Item deleted successfully:', data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}