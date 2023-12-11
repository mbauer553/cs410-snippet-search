let button = document.getElementById('searchbutton');
let input =  document.getElementById('searchtext');
const URL = 'http://<HOSTNAME>:8080/findsnippet?lang=javascript&snippet='
button.addEventListener(
    "click",
    function() {
        fetch(URL+input.value)
        .then(response => response.json())
        .then(
            function(data){
                console.log(data);
            }
        );
    },
    false
);
