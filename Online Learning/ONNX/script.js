const CANVAS_SIZE = 280;
const CANVAS_SCALE = 0.9;

const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
const clearButton = document.getElementById("clear-button");

var myCanvas = document.getElementById("canvas2");
var ctx2 = myCanvas.getContext("2d");
var saveButton = document.getElementById("save-button");

let isMouseDown = false;
let hasIntroText = true;
let lastX = 0;
let lastY = 0;

var sess = new onnx.InferenceSession();
var loadingModelPromise = sess.loadModel("./onnx_model.onnx");
// Load our model.
function load1() {
  var sess = new onnx.InferenceSession();
  var loadingModelPromise = sess.loadModel("./onnx_model.onnx");
  clearCanvas();
}
function load2() {
  var sess = new onnx.InferenceSession();
  var loadingModelPromise = sess.loadModel("./onnx_model2.onnx");
  clearCanvas();
}
function load3() {
  var sess = new onnx.InferenceSession();
  var loadingModelPromise = sess.loadModel("./onnx_model3.onnx");
  clearCanvas();
}

// Add 'Draw a number here!' to the canvas.
ctx.lineWidth = 28;
ctx.lineJoin = "round";
ctx.font = "28px sans-serif";
ctx.textAlign = "center";
ctx.textBaseline = "middle";
ctx.fillStyle = "#212121";
ctx.fillText("Draw a number!", CANVAS_SIZE / 2, CANVAS_SIZE / 2);

// Set the line color for the canvas.
ctx.strokeStyle = "#212121";

function clearCanvas() {
  ctx.clearRect(0, 0, CANVAS_SIZE, CANVAS_SIZE);
  ctx2.clearRect(0, 0, CANVAS_SIZE, CANVAS_SIZE);
}

function drawLine(fromX, fromY, toX, toY) {
  // Draws a line from (fromX, fromY) to (toX, toY).
  ctx.beginPath();
  ctx.moveTo(fromX, fromY);
  ctx.lineTo(toX, toY);
  ctx.closePath();
  ctx.stroke();
  updatePredictions();
}

async function updatePredictions() {
  // Get the predictions for the canvas data.
  const imgData = ctx.getImageData(0, 0, CANVAS_SIZE, CANVAS_SIZE);
  const input = new onnx.Tensor(new Float32Array(imgData.data), "float32");
  var arr = [];
  for (var i = 0; i < 20; i++) {
    arr.push(
      (Math.random() +
        Math.random() +
        Math.random() +
        Math.random() +
        Math.random() +
        Math.random() -
        3) /
        3
    );
  }
  const arr2 = new onnx.Tensor(arr, "float32", [1, 20]);
  await loadingModelPromise;
  const outputMap = await sess.run([input, arr2]);
  const outputTensor = outputMap.values().next().value;
  const predictions = outputTensor.data;
  function splitArray(array, part) {
    var tmp = [];
    for (var i = 0; i < array.length; i += part) {
      tmp.push(array.slice(i, i + part));
    }
    return tmp;
  }
  var arr1 = splitArray(predictions, 28);

  var height = arr1.length;
  var width = arr1[0].length;

  var h = ctx2.canvas.height;
  var w = ctx2.canvas.width;

  var imgData2 = ctx2.getImageData(0, 0, w, h);
  var data = imgData2.data; // the array of RGBA values

  for (var i = 0; i < height; i++) {
    for (var j = 0; j < width; j++) {
      var s = 4 * i * w + 4 * j; // calculate the index in the array
      var x = arr1[i][j]; // the RGB values
      data[s] = x;
      data[s + 1] = x;
      data[s + 2] = x;
      data[s + 3] = 255; // fully opaque
    }
  }

  ctx2.putImageData(imgData2, 0, 0);
}

function downloadURI(uri, name) {
  var link = document.createElement("a");
  link.download = name;
  link.href = uri;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  delete link;
}

function saveCanvas() {
  var resizedCanvas = document.createElement("canvas");
  var resizedContext = resizedCanvas.getContext("2d");

  resizedCanvas.height = "1000";
  resizedCanvas.width = "1000";

  resizedContext.drawImage(myCanvas, 0, 0, 1000, 1000);
  var myResizedData = resizedCanvas.toDataURL();
  // const dataURL = myCanvas.toDataURL();
  downloadURI(myResizedData, "prediction.PNG");
}

function canvasMouseDown(event) {
  isMouseDown = true;
  if (hasIntroText) {
    clearCanvas();
    hasIntroText = false;
  }
  const x = event.offsetX / CANVAS_SCALE;
  const y = event.offsetY / CANVAS_SCALE;

  // To draw a dot on the mouse down event, we set laxtX and lastY to be
  // slightly offset from x and y, and then we call `canvasMouseMove(event)`,
  // which draws a line from (laxtX, lastY) to (x, y) that shows up as a
  // dot because the difference between those points is so small. However,
  // if the points were the same, nothing would be drawn, which is why the
  // 0.001 offset is added.
  lastX = x + 0.001;
  lastY = y + 0.001;
  canvasMouseMove(event);
}

function canvasMouseMove(event) {
  const x = event.offsetX / CANVAS_SCALE;
  const y = event.offsetY / CANVAS_SCALE;
  if (isMouseDown) {
    drawLine(lastX, lastY, x, y);
  }
  lastX = x;
  lastY = y;
}

function bodyMouseUp() {
  isMouseDown = false;
}

function bodyMouseOut(event) {
  // We won't be able to detect a MouseUp event if the mouse has moved
  // ouside the window, so when the mouse leaves the window, we set
  // `isMouseDown` to false automatically. This prevents lines from
  // continuing to be drawn when the mouse returns to the canvas after
  // having been released outside the window.
  if (!event.relatedTarget || event.relatedTarget.nodeName === "HTML") {
    isMouseDown = false;
  }
}

canvas.addEventListener("mousedown", canvasMouseDown);
canvas.addEventListener("mousemove", canvasMouseMove);
document.body.addEventListener("mouseup", bodyMouseUp);
document.body.addEventListener("mouseout", bodyMouseOut);
clearButton.addEventListener("mousedown", clearCanvas);
saveButton.addEventListener("mousedown", saveCanvas);
model1.addEventListener("mousedown", load1);
model2.addEventListener("mousedown", load2);
model3.addEventListener("mousedown", load3);
