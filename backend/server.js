//https://www.freecodecamp.org/news/simplify-your-file-upload-process-in-express-js/
const express = require('express');
const cors = require('cors');
const multer = require('multer');
const app = express();
const {exec} = require('child_process');
const spawn = require('child_process').spawn;
const {stdout, stderr } = require('process');

//Ammend to own machine absolute path
const path_to_combined = "/Users/rossdunn3/Desktop/DissertationPhish/backend/features/combinedModel.py"

app.use(cors());

// multe middleware in handling multipart/form data

const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, 'uploads/');
    },
    filename: (req, file, cb) => {
        cb(null, Date.now() + '-' + file.originalname);
    }
});


const upload = multer({ storage: storage });

// https://stackoverflow.com/questions/62816141/get-the-file-which-send-by-the-multer-in-nodejs

// https://stackoverflow.com/questions/23450534/how-to-call-a-python-function-from-node-js

app.post('/upload', upload.single('file'), (req, res) => {
    if (req.fileValidationError) {
        return res.send("File format error");
    }
    console.log('Uploaded file: ', req.file);
    console.log('File path:', req.file.path);

    const{spawn} = require('child_process');
    const spawnProcess = spawn('python3',[path_to_combined, req.file.path]);
    prediction_data = ""
    outcomeSplit = ""

    spawnProcess.stdout.on('data', function(data) {
        prediction_data += data.toString();
         // https://www.simplilearn.com/tutorials/python-tutorial/split-in-python#:~:text=The%20split()%20function%20can,is%20returned%20as%20the%20output.
         messageSplit = prediction_data.split('||')
         console.log(messageSplit)
         outcomeSplit = messageSplit[1]
    })

    spawnProcess.on('close', function(code){
        
        res.send(outcomeSplit);
    })

    spawnProcess.on('error', (error) => {
        console.error('Failed in spawn processing', error)
    });

    /*Please ammend on another machine, could not work with relative due to path environment issues*/

    /*https://nodejs.org/api/child_process.html*/
});


const port = 20502;
app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});