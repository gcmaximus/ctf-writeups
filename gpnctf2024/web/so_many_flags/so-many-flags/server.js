const express = require('express');
const { exec, spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
const multer = require('multer');
const app = express();

const port = 1337;

const flags = fs.readFileSync('flags.txt', 'utf8')

app.use(express.urlencoded({ extended: true }));
app.use(express.json());

const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, path.join(__dirname, 'uploads'));
  },
  filename: (req, file, cb) => {
    cb(null, Math.random().toString(36).substring(7) + '.html');
  }
});

const upload = multer({ storage });

app.get('/', (req, res) => {
  res.send(`
    <html>
      <body>
        <h1>Upload an HTML file</h1>
        <form action="/submit" method="post" enctype="multipart/form-data">
          <input type="file" name="htmlFile" accept=".html">
          <button type="submit">Submit</button>
        </form>
      </body>
    </html>
  `);
});

app.post('/submit', upload.single('htmlFile'), (req, res) => {

  console.log(req.file);
  const { filename, path: filePath } = req.file;

  if (!filename || !filePath) {
    return res.status(400).send('No file uploaded');
  }

  const userDir = '/tmp/chrome-user-data-dir-' + Math.random().toString(36).substring(7);
  // Don't even try to remove --headless, everything will break. If you want to try stuff, use --remote-debugging-port and disable all other remote debugging flags.
  const command = `bash -c "google-chrome-stable --disable-gpu --headless=new --no-sandbox --no-first-run ${flags} ${filePath}"`;

  res.send('File uploaded and processed successfully. Launched Chrome:<br><br>' + command);

  const chromeProcess = exec(command, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error executing command: ${error.message}\nStdout: ${stdout}`);
    } else {
      console.error(`Stderr: ${stderr}\nStdout: ${stdout}`);
    }
  });

  setTimeout(() => {
    // seems brutal but chrome does Weird Things™ when launched with Every Possible Flag™
    exec('killall -9 chrome', (error, stdout, stderr) => {});
    console.log('Chrome process aborted');
  }, 10_000);
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
