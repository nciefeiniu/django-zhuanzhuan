function disable() {
    inputs = document.getElementById("inputEmail3");
    inputs = inputs.push(document.getElementById("inputText"));
    inputs = inputs.push(document.getElementById("exampleInputFile"));

    for( i=0; i<inputs.length; i++){
        if(inputs[i].value == ""){
            return;
        }
    }
    btn = document.getElementById("tijiao");
    btn.removeAttribute('disabled');
}

disable();
