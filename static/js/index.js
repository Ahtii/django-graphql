


// POPULATE TABLE WITH VEHICLE DATA

var sno = 1;

function create_html_for_table_rows(data){        

    var vehicles = data['vehicles'];

    for (const vehicle in vehicles) {        
        var row_html = "<tr class='table-row'>\
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
            query: "\
                query {\
                    vehicles{\
                        id\
                        name\
                        price\
                        launchDate\
                        vendor {\
                            name\
                        }\
                        category {\
                            name\
                        }\
                    }\
                }\
            "
        })  
    })
    .then(res => res.json())
    .then(data => {    
        console.log(data);
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
    
    // on click of more button
    $(".more-btn").on("click", function(){
        $(".more-menu").toggle();
    });

    // on click of add vendor
    $("#add-vendor").click(function(){
        $(".more-menu").toggle();
        $("#vendor-modal").modal("show");
    });

    // on click of add category
    $("#add-category").click(function(){
        $(".more-menu").toggle();
        $("#category-modal").modal("show");
    });

    // on click of add vehicle
    $("#add-vehicle").click(function(){
        $(".more-menu").toggle();
        $("#vehicle-modal").modal("show");
    });

    // on vendor form submit 
    $("#vendor-form").submit(function(e){
        e.preventDefault();        
        var value = $("#vendor-input").val();
        console.log(value);
        if (value){
            fetch("http://localhost:8000/custom_graphql", {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": $('#vendor-form input[name=csrfmiddlewaretoken]').val()
                },
                body: JSON.stringify(
                    {
                        query: "\
                            mutation addVendor($name: String!){\
                                addVendor(name: $name){\
                                    vendor {\
                                        id\
                                        name\
                                    }\
                                }\
                            }\
                        ",
                        variables: {"name": value}
                    }
                )  
            })
            .then(res => res.json())
            .then(data => {    
                console.log("got saved :)");                
                if (data == null)
                    alert("Error occured!");                
                else {
                    $("#vendor-modal .close").trigger("click");
                }    
            })             
        }
    });

    // on category form submit 
    $("#category-form").submit(function(e){
        e.preventDefault();        
        var value = $("#category-input").val();
        console.log(value);
        if (value){
            fetch("http://localhost:8000/custom_graphql", {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": $('#category-form input[name=csrfmiddlewaretoken]').val()
                },
                body: JSON.stringify(
                    {
                        query: "\
                            mutation addCategory($name: String!){\
                                addCategory(name: $name){\
                                    category {\
                                        id\
                                        name\
                                    }\
                                }\
                            }\
                        ",
                        variables: {"name": value}
                    }
                )  
            })
            .then(res => res.json())
            .then(data => {    
                console.log("got saved :)");                
                if (data == null)
                    alert("Error occured!");                
                else {
                    $("#category-modal .close").trigger("click");
                }    
            })             
        }
    });

    // on vehicle form submit 
    $("#vehicle-form").submit(function(e){
        e.preventDefault();   
        var inputs = {
            name: $("#vehicle-name-input").val(),
            price: $("#vehicle-price-input").val(),
            date: $("#vehicle-date-input").val(),
            vendor: $("#vehicle-vendor-input").val(),
            category: $("#vehicle-category-input").val()
        }     
        if (inputs['name'] || inputs['price'] || inputs['date'] || inputs['vendor'] || inputs['category']){
            fetch("http://localhost:8000/custom_graphql", {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": $('#category-form input[name=csrfmiddlewaretoken]').val()
                },
                body: JSON.stringify(
                    {
                        query: "\
                            mutation addVehicle($name: String!, $price: Decimal!, $launchDate: Date!, $vendor: String!, $category: String!){\
                                addVehicle(name: $name, price: $price, launchDate: $launchDate, vendor: $vendor, category: $category){\
                                        vehicle {\
                                            id\
                                            name\
                                            price\
                                            launchDate\
                                            vendor {\
                                                name\
                                            }\
                                            category {\
                                                name\
                                            }\
                                        }\
                                }\
                            }\
                        ",
                        variables: {
                            "name": inputs['name'],
                            "price": inputs['price'],
                            "launchDate": inputs['date'],
                            "vendor": inputs['vendor'],
                            "category": inputs['category']
                        }
                    }
                )  
            })
            .then(res => res.json())
            .then(data => {                                   
                if (data == null)
                    alert("Error occured!");                
                else {
                    var row_html = "<tr class='table-row'>\
                            <th scope='row'>"+sno+"</th>\
                            <td>"+data['addVehicle']['vehicle']['id']+"</td>\
                            <td>"+data['addVehicle']['vehicle']['name']+"</td>\
                            <td>"+data['addVehicle']['vehicle']['price']+" lakh</td>\
                            <td>"+data['addVehicle']['vehicle']['launchDate']+"</td>\
                            <td>"+data['addVehicle']['vehicle']['vendor']['name']+"</td>\
                            <td>"+data['addVehicle']['vehicle']['category']['name']+"</td>\
                        </tr>";  
                    
                    sno += 1;
                    $(".table-body").append(row_html);
                    $("#vehicle-modal .close").trigger("click");
                }    
            })             
        }
    });
});
