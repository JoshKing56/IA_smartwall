const express = require('express');
const app = express();
const path = require('path');
const fs = require('fs');

const bodyParser = require('body-parser');
app.use(bodyParser.json());

var current_data = {"src": {'a': 1, 'b':1}, "ref": {'a':'Bluetooth', 'b':'Bluetooth'}}

let item_data = fs.readFileSync('./items.json');  
let item_translation = JSON.parse(item_data);

let anim_data = fs.readFileSync('./anims.json');  
let anims_matrix = JSON.parse(anim_data);

// Post data format: {a: INT, b:INT}
app.post('/update', (req, res, next)=>{
    current_data.src = req.body;
    
    anim_data_item = anims_matrix[`${current_data.src.a}+${current_data.src.b}`] 
    
    if(anim_data_item != undefined){
        current_data.src['c'] = anim_data_item.src
    }
    
    current_data.ref = {
        'a': item_translation[current_data.src.a], 
        'b': item_translation[current_data.src.b],
        'c': anim_data_item.msg
    }

    io.emit('new_match', current_data, {for: 'everyone'});
    res.sendStatus(200)
})

app.get('/', function(req, res){
    res.sendFile(__dirname + '/index.html');
});

app.use(express.static(path.join(__dirname, 'public'))); 

const server = app.listen(process.env.PORT || 3000);

const io = require('socket.io').listen(server);  

io.on('connection', (socket) => {
    console.log('IO: The frontend viewport has connected');
    // console.log("DATA: " + JSON.stringify(data));
    io.emit('new_match', current_data);

    socket.on('disconnect', function(){
        console.log('IO: The frontend viewport has disconnected');
    });
});