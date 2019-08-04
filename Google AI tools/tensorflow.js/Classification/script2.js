/**
 * We first load the Swedish Car Insurance dateset and then we select the variables we are interested in.
 * Successively, we get rid of any missing data.
 */

async function getData() {
  const wineDataReq = await fetch(
    "https://raw.githubusercontent.com/pierpaolo28/Artificial-Intelligence-Projects/master/Google%20AI%20tools/tensorflow.js/wines.json"
  );
  const wineData = await wineDataReq.json();
  const cleaned = wineData
    .map(wine => ({
      fixed: wine.fixed_acidity,
      volatile: wine.volatile_acidity,
      citric: wine.citric_acid,
      sugar: wine.residual_sugar,
      chlorides: wine.chlorides,
      free: wine.free_sulfur_dioxide,
      total: wine.total_sulfur_dioxide,
      density: wine.density,
      ph: wine.pH,
      sulphates: wine.sulphates,
      alcohol: wine.alcohol,
      quality: wine.quality,
      label: wine.style
    }))
    .filter(
      wine =>
        wine.fixed != null &&
        wine.volatile != null &&
        wine.citric != null &&
        wine.sugar != null &&
        wine.chlorides != null &&
        wine.free != null &&
        wine.total != null &&
        wine.density != null &&
        wine.ph != null &&
        wine.sulphates != null &&
        wine.alcohol != null &&
        wine.quality != null &&
        wine.label != null
    );

  return cleaned;
}

async function run() {
  // Load and plot the original input data that we are going to train on.
  const data = await getData();
  values = data.map(d => ({
    x: d.alcohol,
    y: d.quality
  }));

  tfvis.render.scatterplot(
    { name: "Alcohol vs Quality" },
    { values },
    {
      xLabel: "Alcohol",
      yLabel: "Quality",
      height: 300
    }
  );

  values = data.map(d => ({
    x: d.chlorides,
    y: d.quality
  }));

  tfvis.render.scatterplot(
    { name: "Chlorides vs Quality" },
    { values },
    {
      xLabel: "Alcohol",
      yLabel: "Quality",
      height: 300
    }
  );

  values = data.map(d => ({
    x: d.citric,
    y: d.quality
  }));

  tfvis.render.scatterplot(
    { name: "Citric vs Quality" },
    { values },
    {
      xLabel: "Citric",
      yLabel: "Quality",
      height: 300
    }
  );

  // Create the model
  const model = createModel();
  const cont = { name: "Model Summary", tab: "Model Training" };
  tfvis.show.modelSummary(cont, model);
  const surface = { name: "Layer Summary", tab: "Model Training" };
  tfvis.show.layer(surface, model.getLayer(undefined, 1));

  // Convert the data to a form we can use for training.
  const tensorData = convertToTensor(data);
  const { inputs, labels } = tensorData;

  // Train the model
  await trainModel(model, inputs, labels);
  console.log("Done Training");

  //await doPrediction(model, inputs, labels);
  await evaluateModelFunction(model, inputs, data.map(d => d.label));
  await showAccuracy(model, inputs, data.map(d => d.label));
  await showConfusion(model, inputs, data.map(d => d.label));
}

async function trainModel(model, inputs, labels) {
  // Prepare the model for training.
  model.compile({
    optimizer: tf.train.adam(),
    loss: "categoricalCrossentropy",
    metrics: ["acc", "mse"]
  });

  const batchSize = 512;
  const epochs = 5;
  const cont2 = { name: "Training Progresses", tab: "Model Training" };
  return await model.fit(inputs, labels, {
    batchSize,
    epochs,
    shuffle: true,
    callbacks: tfvis.show.fitCallbacks(cont2, ["loss", "acc", "mse"], {
      height: 200,
      callbacks: ["onEpochEnd"]
    })
  });
}

async function evaluateModelFunction(model, inputs, labels) {
  const [preds, labels3] = doPrediction(model, inputs, labels);
  const result = await tfvis.metrics.accuracy(labels3, preds);
  console.log("The overall model accuracy is: ", result);
  const surface = { name: "Predictions Distribution", tab: "Evaluation" };
  await tfvis.show.valuesDistribution(surface, preds);
}

const classNames = ["Red", "White"];

async function showAccuracy(model, input, labels) {
  const [preds, labels2] = doPrediction(model, input, labels);
  const classAccuracy = await tfvis.metrics.perClassAccuracy(labels2, preds);
  const container = { name: "Accuracy", tab: "Evaluation" };
  tfvis.show.perClassAccuracy(container, classAccuracy, classNames);
}

async function showConfusion(model, input, labels) {
  const [preds, labels3] = doPrediction(model, input, labels);
  const confusionMatrix = await tfvis.metrics.confusionMatrix(labels3, preds);
  const container = { name: "Confusion Matrix", tab: "Evaluation" };
  tfvis.render.confusionMatrix(
    container,
    { values: confusionMatrix },
    classNames
  );
}

/**
 * Convert the input data to tensors that we can use for machine
 * learning. We will also do the important best practices of _shuffling_
 * the data and _normalizing_ it.
 */
function convertToTensor(data) {
  // Wrapping these calculations in a tidy will dispose any
  // intermediate tensors.

  return tf.tidy(() => {
    // Step 1. Shuffle the data
    tf.util.shuffle(data);

    // Step 2. Convert data to Tensor
    const inputs = data.map(d => [
      d.fixed,
      d.volatile,
      d.citric,
      d.sugar,
      d.chlorides,
      d.free,
      d.total,
      d.density,
      d.ph,
      d.sulphates,
      d.alcohol,
      d.quality
    ]);
    const labels = data.map(d => d.label);

    const inputTensor = tf.tensor2d(inputs, [inputs.length, inputs[0].length]);
    const labelTensor = tf.oneHot(tf.tensor1d(labels, "int32"), 2);
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

  // Add 3 hidden layers
  model.add(tf.layers.dense({ inputShape: [12], units: 8, useBias: true }));
  model.add(tf.layers.dense({ units: 50, useBias: true }));
  model.add(tf.layers.dense({ units: 10, useBias: true }));
  // Add an output layer
  model.add(tf.layers.dense({ units: 2, useBias: true }));

  return model;
}

function doPrediction(model, input, labels) {
  const out = tf.tensor1d(labels, "int32");
  const xs = input;
  const preds = model.predict(xs.reshape([6497, 12])).argMax([-1]);
  return [preds, out];
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

document.addEventListener("DOMContentLoaded", function() {
  run();
  setupListeners();
});
