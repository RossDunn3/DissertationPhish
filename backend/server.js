//https://www.freecodecamp.org/news/simplify-your-file-upload-process-in-express-js/
const express = require('express');
const cors = require('cors');
const multer = require('multer');
const app = express();
const {exec} = require('child_process');
const { stdout, stderr } = require('process');

const path_to_predict = "/Users/rossdunn3/Desktop/DissertationPhish/backend/features/combinedModel.py";

app.use(cors());

const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, 'uploads/');
    },
    filename: (req, file, cb) => {
        cb(null, Date.now() + '-' + file.originalname);
    }
});

function fileFiltering(req, file, cb) {
    if (!file.originalname.match(/\.(txt)$/)) {
        req.fileValidationError = "This server only allows the upload of txt, eml, or msg files";
        return cb(new Error('Server only allows txt, eml, or msg'), false);
    }
    cb(null, true)
}

const upload = multer({ storage: storage });

// https://stackoverflow.com/questions/62816141/get-the-file-which-send-by-the-multer-in-nodejs

app.post('/upload', upload.single('file'), (req, res) => {
    if (req.fileValidationError) {
        return res.send("File format error");
    }
    console.log('Uploaded file: ', req.file);
    console.log('File path:', req.file.path);

    const path_to_combined = "/Users/rossdunn3/Desktop/DissertationPhish/backend/features/combinedModel.py"

    exec(`python3 ${path_to_combined}`, (error, stdout,stderr) => {
        if(error){
            console.error(`arghh error  ${error}`)
            return
        }
        console.log(`combined prediction is: ${stdout}`);
        
        // we only want to get the final outcome, not the progress bar
        // https://www.simplilearn.com/tutorials/python-tutorial/split-in-python#:~:text=The%20split()%20function%20can,is%20returned%20as%20the%20output.
        messageSplit = stdout.split("||")

        phishOutcome = messageSplit[1];

        res.send(phishOutcome)
    });
});

const port = 20502;
app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});