/**
 * We first load the Swedish Car Insurance dateset and then we select the variables we are interested in.
 * Successively, we get rid of any missing data.
 */

async function getData() {
  const pimaDataReq = await fetch(
    "https://raw.githubusercontent.com/pierpaolo28/Artificial-Intelligence-Projects/master/Google%20AI%20tools/tensorflow.js/pimadata.json"
  );
  const pimaData = await pimaDataReq.json();
  const cleaned = pimaData
    .map(pima => ({
      pregnancies: pima.Pregnancies,
      glucose: pima.Glucose,
      blood: pima.BloodPressure,
      skin: pima.SkinThickness,
      insulin: pima.Insulin,
      bmi: pima.BMI,
      diabetes: pima.DiabetesPedigreeFunction,
      age: pima.Age,
      label: pima.Outcome
    }))
    .filter(
      pima =>
        pima.pregnancies != null &&
        pima.glucose != null &&
        pima.blood != null &&
        pima.skin != null &&
        pima.insulin != null &&
        pima.bmi != null &&
        pima.diabetes != null &&
        pima.age != null &&
        pima.label != null
    );

  return cleaned;
}

async function run() {
  // Load and plot the original input data that we are going to train on.
  const data = await getData();
  values = data.map(d => ({
    x: d.insulin,
    y: d.blood
  }));

  tfvis.render.scatterplot(
    { name: "Insulin vs Blood Pressure" },
    { values },
    {
      xLabel: "Insulin",
      yLabel: "Blood Pressure",
      height: 300
    }
  );

  values = data.map(d => ({
    x: d.insulin,
    y: d.glucose
  }));

  tfvis.render.scatterplot(
    { name: "Insulin vs Glucose" },
    { values },
    {
      xLabel: "Insulin",
      yLabel: "Glucose",
      height: 300
    }
  );

  values = data.map(d => ({
    x: d.pregnancies,
    y: d.diabetes
  }));

  tfvis.render.scatterplot(
    { name: "Pregnancies vs Diabetes" },
    { values },
    {
      xLabel: "Pregnancies",
      yLabel: "Diabetes",
      height: 300
    }
  );

  // Convert the data to a form we can use for training.
  const tensorData = convertToTensor(data);
  const { inputs, labels } = tensorData;

  const model = await tf.loadLayersModel(
    "https://raw.githubusercontent.com/pierpaolo28/Artificial-Intelligence-Projects/master/Google%20AI%20tools/tensorflow.js/modelready/model.json"
  );
  const cont = { name: "Model Summary", tab: "Model Training" };
  tfvis.show.modelSummary(cont, model);
  const surface = { name: "Layer Summary", tab: "Model Training" };
  tfvis.show.layer(surface, model.getLayer(undefined, 1));

  await evaluateModelFunction(model, inputs, data.map(d => d.label));
  await showAccuracy(model, inputs, data.map(d => d.label));
  await showConfusion(model, inputs, data.map(d => d.label));
}

async function evaluateModelFunction(model, inputs, labels) {
  const [preds, labels3] = doPrediction(model, inputs, labels);
  const result = await tfvis.metrics.accuracy(labels3, preds);
  console.log("The overall model accuracy is: ", result);
  //   const surface = { name: "Predictions Distribution", tab: "Evaluation" };
  //   await tfvis.show.valuesDistribution(surface, preds);
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
      d.pregnancies,
      d.glucose,
      d.blood,
      d.skin,
      d.insulin,
      d.bmi,
      d.diabetes,
      d.age
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

function doPrediction(model, input, labels) {
  const out = tf.tensor1d(labels, "int32");
  const xs = input;
  const preds = model.predict(xs.reshape([768, 8])).argMax([-1]);
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
