/**
 * We first load the Swedish Car Insurance dateset and then we select the variables we are interested in.
 * Successively, we get rid of any missing data.
 */

async function getData() {
  const insuranceDataReq = await fetch(
    "https://raw.githubusercontent.com/pierpaolo28/Artificial-Intelligence-Projects/master/Google%20AI%20tools/tensorflow.js/swedish.json"
  );
  const insuranceData = await insuranceDataReq.json();
  const cleaned = insuranceData
    .map(insurance => ({
      claims: insurance.X,
      payment: insurance.Y
    }))
    .filter(insurance => insurance.claims != null && insurance.payment != null);

  return cleaned;
}

async function run() {
  // Load and plot the original input data that we are going to train on.
  const data = await getData();
  const values = data.map(d => ({
    x: d.claims,
    y: d.payment
  }));

  tfvis.render.scatterplot(
    { name: "Number of claims vs Total Payment" },
    { values },
    {
      xLabel: "Number of claims",
      yLabel: "Total Payment",
      height: 300
    }
  );

  // Create the model
  const model = createModel();
  tfvis.show.modelSummary({ name: "Model Summary" }, model);

  // Convert the data to a form we can use for training.
  const tensorData = convertToTensor(data);
  const { inputs, labels } = tensorData;

  // Train the model
  await trainModel(model, inputs, labels);
  console.log("Done Training");

  // Make some predictions using the model and compare them to the
  // original data
  testModel(model, inputs, data, tensorData);

  evaluateModelFunction(model, inputs, data.map(d => d.label));
}

async function trainModel(model, inputs, labels) {
  // Prepare the model for training.
  model.compile({
    optimizer: tf.train.adam(),
    loss: tf.losses.meanSquaredError,
    metrics: ["mse"]
  });

  const batchSize = 32;
  const epochs = 50;

  return await model.fit(inputs, labels, {
    batchSize,
    epochs,
    shuffle: true,
    callbacks: tfvis.show.fitCallbacks(
      { name: "Training Progresses" },
      ["loss", "mse"],
      { height: 200, callbacks: ["onEpochEnd"] }
    )
  });
}

async function evaluateModelFunction(model, inputs, labels) {
  const [preds, labels1] = doPrediction(model, inputs, labels);
  const result = await tfvis.metrics.accuracy(labels1, preds);
  console.log("The overall model accuracy is: ", result);
}

function setupListeners() {
  document.querySelector("#show-visor").addEventListener("click", () => {
    const visorInstance = tfvis.visor();
    if (!visorInstance.isOpen()) {
      visorInstance.toggle();
    }
  });

  document.querySelector("#hide-visor").addEventListener("click", () => {
    const visorInstance = tfvis.visor();
    if (visorInstance.isOpen()) {
      visorInstance.toggle();
    }
  });
}

/**
 * Convert the input data to tensors that we can use for machine
 * learning. We will also do the important best practices of _shuffling_
 * the data and _normalizing_ the claims data
 * on the y-axis.
 */
function convertToTensor(data) {
  // Wrapping these calculations in a tidy will dispose any
  // intermediate tensors.

  return tf.tidy(() => {
    // Step 1. Shuffle the data
    tf.util.shuffle(data);

    // Step 2. Convert data to Tensor
    const inputs = data.map(d => d.claims);
    const labels = data.map(d => d.payment);

    const inputTensor = tf.tensor2d(inputs, [inputs.length, 1]);
    const labelTensor = tf.tensor2d(labels, [labels.length, 1]);

    //Step 3. Normalize the data to the range 0 - 1 using min-max scaling
    const inputMax = inputTensor.max();
    const inputMin = inputTensor.min();
    const labelMax = labelTensor.max();
    const labelMin = labelTensor.min();

    const normalizedInputs = inputTensor
      .sub(inputMin)
      .div(inputMax.sub(inputMin));
    const normalizedLabels = labelTensor
      .sub(labelMin)
      .div(labelMax.sub(labelMin));

    return {
      inputs: normalizedInputs,
      labels: normalizedLabels,
      // Return the min/max bounds so we can use them later.
      inputMax,
      inputMin,
      labelMax,
      labelMin
    };
  });
}

function createModel() {
  // Create a sequential model
  const model = tf.sequential();

  // Add two hidden layers
  model.add(tf.layers.dense({ inputShape: [1], units: 5, useBias: true }));
  model.add(tf.layers.dense({ units: 10, useBias: true }));
  // Add an output layer
  model.add(tf.layers.dense({ units: 1, useBias: true }));

  return model;
}

function doPrediction(model, input, labels) {
  const out = tf.tensor1d(labels, "int32");
  const xs = input;
  const preds = model.predict(xs.reshape([63, 1])).argMax([-1]);
  return [preds, out];
}

function testModel(model, input, inputData, normalizationData) {
  const { inputMax, inputMin, labelMin, labelMax } = normalizationData;

  // Generate predictions for a uniform range of numbers between 0 and 1;
  // We un-normalize the data by doing the inverse of the min-max scaling
  // that we did earlier.
  const [xs, preds] = tf.tidy(() => {
    //const xs = tf.linspace(0, 1, 63); //Using same fake data to test the model
    const xs = input; // Using the input data to test the model
    const preds = model.predict(xs.reshape([63, 1]));

    const unNormXs = xs.mul(inputMax.sub(inputMin)).add(inputMin);

    const unNormPreds = preds.mul(labelMax.sub(labelMin)).add(labelMin);

    // Un-normalize the data
    return [unNormXs.dataSync(), unNormPreds.dataSync()];
  });

  const predictedPoints = Array.from(xs).map((val, i) => {
    return { x: val, y: preds[i] };
  });

  const originalPoints = inputData.map(d => ({
    x: d.claims,
    y: d.payment
  }));

  tfvis.render.scatterplot(
    { name: "Model Predictions vs Original Data" },
    {
      values: [originalPoints, predictedPoints],
      series: ["original", "predicted"]
    },
    {
      xLabel: "Number of claims",
      yLabel: "Total Payment",
      height: 300
    }
  );
}

document.addEventListener("DOMContentLoaded", function() {
  run();
  setupListeners();
});
