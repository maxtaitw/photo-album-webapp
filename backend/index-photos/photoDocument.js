function normalizeLabel(label) {
  return String(label).trim().toLowerCase();
}

function parseCustomLabels(value) {
  if (!value) {
    return [];
  }

  return String(value)
    .split(",")
    .map(normalizeLabel)
    .filter(Boolean);
}

function normalizeRekognitionLabels(labels) {
  if (!Array.isArray(labels)) {
    return [];
  }

  return labels
    .map((label) => {
      if (typeof label === "string") {
        return label;
      }

      return label && label.Name;
    })
    .filter(Boolean)
    .map(normalizeLabel)
    .filter(Boolean);
}

function mergeLabels(rekognitionLabels, customLabels) {
  return Array.from(
    new Set([
      ...normalizeRekognitionLabels(rekognitionLabels),
      ...parseCustomLabels(customLabels)
    ])
  );
}

function buildPhotoDocument({ bucket, objectKey, createdTimestamp, labels }) {
  return {
    objectKey,
    bucket,
    createdTimestamp,
    labels
  };
}

module.exports = {
  buildPhotoDocument,
  mergeLabels,
  parseCustomLabels
};
