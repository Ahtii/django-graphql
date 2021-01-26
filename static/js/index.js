

// POPULATE TABLE WITH VEHICLE DATA

function create_html_for_table_rows(data){        

    var vehicles = data['vehicles']
    var sno = 1;

    for (const vehicle in vehicles) {        
        var row_html = "<tr>\
                            <th scope='row'>"+sno+"</th>\
                            <td>"+vehicles[vehicle]['id']+"</td>\
                            <td>"+vehicles[vehicle]['name']+"</td>\
                            <td>"+vehicles[vehicle]['price']+" lakh</td>\
                            <td>"+vehicles[vehicle]['launchDate']+"</td>\
                            <td>"+vehicles[vehicle]['vendor']['name']+"</td>\
                            <td>"+vehicles[vehicle]['category']['name']+"</td>\
                        </tr>";  
                    
        sno += 1;
        $(".table-body").append(row_html);
    }
}

// get csrftoken from cookie

function get_cookie(name){
    let cookie_value = null;
    if (document.cookie && document.cookie !== ''){
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++){
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')){
                cookie_value = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookie_value;
}


// GET ALL VEHICLES

$(document).ready(function(){
    // after page refresh
    const csrftoken = get_cookie('csrftoken')
    fetch('http://localhost:8000/custom_graphql', {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify({
            query: `
                query {
                    vehicles {
                        id
                        name
                        price
                        launchDate
                        vendor {
                            name
                        }
                        category {
                            name
                        }
                    }
                }
            `
        })  
    })
    .then(res => res.json())
    .then(data => {    
        create_html_for_table_rows(data)    
    })
    // after new data is avialible  
    fetch('http://localhost:8000/custom_graphql', {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify({
            query: "\
                subscription {\
                    vendorUpdated {\
                        id\
                        name\
                    }\
                }\
            "
        })  
    })
    .then(res => res.json())
    .then(data => {    
        //create_html_for_table_rows(data)    
        console.log(data);
    })      
});
