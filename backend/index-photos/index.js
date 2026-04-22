exports.handler = async (event) => {
  const records = event.Records || [];

  const photos = records.map((record) => {
    const bucket = record.s3 && record.s3.bucket && record.s3.bucket.name;
    const objectKey = record.s3 && record.s3.object && record.s3.object.key;

    return {
      bucket,
      objectKey: objectKey ? decodeURIComponent(objectKey.replace(/\+/g, " ")) : undefined,
      eventTime: record.eventTime
    };
  });

  return {
    statusCode: 200,
    body: JSON.stringify({
      message: "index-photos handler received S3 upload event",
      photos
    })
  };
};
