function submitRequest() {
    var location = document.getElementById('location').value;
    var description = document.getElementById('description').value;

    // In a real application, you would send this data to a server for processing
    // For now, we'll just display an alert
    alert("Request Submitted!\n\nLocation: " + location + "\nDescription: " + description);
}



getElementById(divId).scrollIntoView({ behavior: 'smooth' })