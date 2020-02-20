% https://uk.mathworks.com/help/vision/examples/image-category-classification-using-bag-of-features.html
imds = imageDatastore('training','IncludeSubfolders',true,'LabelSource','foldernames');
tbl = countEachLabel(imds)
[trainingSet, validationSet] = splitEachLabel(imds, 0.8, 'randomize');
bag = bagOfFeatures(trainingSet);
img = readimage(imds, 1);
featureVector = encode(bag, img);

% Plot the histogram of visual word occurrences
figure
bar(featureVector)
title('Visual word occurrences')
xlabel('Visual word index')
ylabel('Frequency of occurrence')
categoryClassifier = trainImageCategoryClassifier(trainingSet, bag);
confMatrix = evaluate(categoryClassifier, trainingSet);
confMatrix = evaluate(categoryClassifier, validationSet);
mean(diag(confMatrix))