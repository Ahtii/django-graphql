

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


// GET ALL VEHICLES

$(document).ready(function(){
    fetch('http://localhost:8000/query', {
        method: 'POST',
        headers: {"Content-Type": "application/json"},
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
});
