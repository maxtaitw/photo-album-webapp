const assert = require("assert");

const {
  buildPhotoDocument,
  mergeLabels,
  parseCustomLabels
} = require("./photoDocument");

assert.deepStrictEqual(parseCustomLabels("Sam, Sally"), ["sam", "sally"]);
assert.deepStrictEqual(parseCustomLabels("  Sam  , , Sally "), ["sam", "sally"]);
assert.deepStrictEqual(parseCustomLabels(""), []);
assert.deepStrictEqual(parseCustomLabels(undefined), []);

assert.deepStrictEqual(
  mergeLabels([{ Name: "Dog" }, { Name: "Park" }], "dog, Ball"),
  ["dog", "park", "ball"]
);

assert.deepStrictEqual(
  mergeLabels(["Tree", "tree", "Bird"], "bird, sky"),
  ["tree", "bird", "sky"]
);

assert.deepStrictEqual(
  buildPhotoDocument({
    bucket: "photo-album-storage-bucket",
    objectKey: "sample-photo.jpg",
    createdTimestamp: "2026-04-22T12:40:02.000Z",
    labels: ["tree", "bird"]
  }),
  {
    objectKey: "sample-photo.jpg",
    bucket: "photo-album-storage-bucket",
    createdTimestamp: "2026-04-22T12:40:02.000Z",
    labels: ["tree", "bird"]
  }
);

console.log("photoDocument tests passed");
